# -*- coding: utf-8 -*-
from functools import wraps
from flask import session
import pandas as pd
import sqlite3 as sql

# constants
ALLOWED_EXTENSIONS = set(["xlsx"])
UPLOAD_FOLDER = "uploads/"

DB_NAME = "database.db"

CONTEST_TYPES = ("project", "poster", "popularity")

PROJECT_QUESTIONS_FILENAME = "questions_project.txt"
POSTER_QUESTIONS_FILENAME = "questions_poster.txt"


# file handling
def allowed_file(filename):
    return any(filename.lower().endswith("." + ext.lower())
               for ext in ALLOWED_EXTENSIONS)


# get questions
def project_questions():
    with open(PROJECT_QUESTIONS_FILENAME) as f:
        questions = [q for q in f]
    return questions


def poster_questions():
    with open(POSTER_QUESTIONS_FILENAME) as f:
        questions = [q for q in f]
    return questions


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

    # table for contests
    cur.execute("CREATE TABLE IF NOT EXISTS contests"
                "(name TEXT NOT NULL UNIQUE,"
                "type TEXT NOT NULL,"
                "filename TEXT NOT NULL,"
                "num_judges integer,"
                "judges TEXT)")

    # table for scores
    # scores are separated by ","
    cur.execute("CREATE TABLE IF NOT EXISTS scores"
                "(contest TEXT NOT NULL,"
                "project TEXT NOT NULL,"
                "judge TEXT NOT NULL,"
                "scores TEXT NOT NULL,"
                "UNIQUE(contest, project))")

    conn.commit()
    conn.close()


def create_judges_table(contest_name):
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS judges" + str(contest_name) +
                "(username TEXT NOT NULL UNIQUE,"
                "company TEXT,"
                "real_name TEXT,"
                "projects TEXT)")

    conn.commit()
    conn.close()


def create_projects_table(contest_name):
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS projects" + str(contest_name) +
                "(id TEXT NOT NULL UNIQUE,"
                "title TEXT NOT NULL UNIQUE,"
                "company TEXT,"
                "sponsor TEXT,"
                "instructor TEXT,"
                "course TEXT,"
                "names TEXTL,"
                "table TEXT,"
                "judges TEXT)")

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

    df = pd.DataFrame(cur.fetchall(), columns=cols)

    conn.close()

    return df


def get_projects_for_judge(judge):
    """Get a list of the projects assigned to judge."""
    df = get_table("judges")

    if not df.empty:
        return list(df[df["judge"] == judge]["projects"])
    else:
        return ["NONE"]


# authentication
def get_user_access_level(username):
    df = get_table("users")

    if not df.empty:
        return df[df["username"] == username]["access_level"].item()
    else:
        return None


def required_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if "username" in session:
                level = get_user_access_level(session["username"])

                if level == access_level:
                    return f(*args, **kwargs)
                else:
                    return "cannot access"
            else:
                return "not logged in"
        return wrap
    return decorator


def validate(username, password):
    df = get_table("users")

    if not df.empty:
        return (df[df["username"] == username]["password"].item() == password)
    else:
        return False
