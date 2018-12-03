# -*- coding: utf-8 -*-
from functools import wraps
from flask import session
import pandas as pd
import sqlite3 as sql

DB_NAME = "database.db"


# database functions

def init_db():
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()

    # table for users
    cur.execute("CREATE TABLE IF NOT EXISTS users"
                "(username TEXT NOT NULL UNIQUE,"
                "password TEXT NOT NULL,"
                "access_level integer NOT NULL)")
    cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)",
                ("admin", "password", 2))
    cur.execute("INSERT OR IGNORE INTO users VALUES (?,?,?)",
                ("judge1", "password", 1))

    # table for list of projects
    # projects are seperated by ","
    cur.execute("CREATE TABLE IF NOT EXISTS judge_projects"
                "(judge TEXT NOT NULL,"
                "projects TEXT NOT NULL)")

    # table for project scoring
    # scores are sepearted by ","
    cur.execute("CREATE TABLE IF NOT EXISTS project_scores"
                "(judge TEXT NOT NULL,"
                "project TEXT NOT NULL,"
                "scores TEXT NOT NULL)")

    conn.commit()
    conn.close()


def drop_table(table):
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS (?)", table)
    cur.commit()
    conn.close()


def get_table(table):
    """Get a pandas DataFrame object representing the table."""
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT * FROM " + table)
    cols = [c[0] for c in cur.description]

    return pd.DataFrame(cur.fetchall(), columns=cols)


def get_projects_for_judge(judge):
    df = get_table("judge_projects")

    if not df.empty:
        return list(df[df["judge"] == judge]["projects"])
    else:
        return []


# get access_level for account
def get_user_access_level(username):
    df = get_table("users")

    if not df.empty:
        return df[df["username"] == username]["access_level"].get_value(0)
    else:
        return None


# other

def validate(username, password):
    df = get_table("users")

    if not df.empty:
        return (df[df["username"] == username]["password"].get_value(0) ==
                password)
    else:
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
