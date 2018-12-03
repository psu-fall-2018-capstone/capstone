# -*- coding: utf-8 -*-
from functools import wraps
from flask import session
import sqlite3 as sql


# database functions

def init_db():
    conn = sql.connect("database.db")
    cur = conn.cursor()

    # table for users
    cur.execute("""CREATE TABLE IF NOT EXISTS users
        (username TEXT NOT NULL,
         password TEXT NOT NULL,
         access_level integer NOT NULL)""")
    cur.execute("INSERT INTO users VALUES (?,?,?)", ("admin", "password", 2))
    cur.execute("INSERT INTO users VALUES (?,?,?)", ("judge1", "password", 1))

    # table for list of projects 
    # projects are seperated by ","
    cur.execute("""CREATE TABLE IF NOT EXISTS judge_projects
        (judge TEXT NOT NULL,
         projects TEXT NOT NULL)""")

    # table for project scoring
    # scores are sepearted by ","
    cur.execute("""CREATE TABLE IF NOT EXISTS project_scores
        (judge TEXT NOT NULL,
         project TEXT NOT NULL,
         scores TEXT NOT NULL)""")

    conn.commit()
    conn.close()

def drop_table(table):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS (?)", table)
    cur.commit()
    conn.close()

# get project list for judge by username
def get_projects_for_judge(judge):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT projects FROM judge_projects WHERE judge=?", (judge,))
    projects = cur.fetchone()
    conn.close()

    if projects:
        return projects[0]
    else:
        return []
    

# get access_level for account
def get_user_access_level(username):
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT access_level FROM users WHERE username=?", (username,))
    access_level = cur.fetchone()
    conn.close()

    return access_level[0]


# other

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
                level = get_user_access_level(session["username"])

                if level == access_level:
                    return f(*args, **kwargs)
                else:
                    return "cannot access"
            else:
                return "not logged in"
        return wrap
    return decorator
