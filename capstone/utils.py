# -*- coding: utf-8 -*-
from functools import wraps
from flask import session
import sqlite3 as sql

#######################################
### Database functions
#######################################

def init_db():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute('''CREATE TABLE users 
        (username TEXT NOT NULL, 
         password TEXT NOT NULL,
         access_level integer NOT NULL)''')
    cur.execute("INSERT INTO users VALUES (?,?,?)", ("admin", "password", 2))
    conn.commit()
    conn.close()


def get_user_access_level(username):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT access_level FROM users WHERE username=?", (username,))
    access_level = cur.fetchone()
    conn.close()

    return access_level[0]

#######################################
### other
#######################################

def validate(username, password):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    check = cur.fetchone()
    conn.close()

    if check:
        dbPass = check[0]
        if password == dbPass:
            return True
    return False


def required_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if "user" in session:
                level = get_user_access_level(session["user"])

                if level == access_level:
                    return f(*args, **kwargs)
                else:
                    return "cannot access"
            else:
                return "not logged in"
        return wrap
    return decorator