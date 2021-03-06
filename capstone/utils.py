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

    # table for contests
    cur.execute("CREATE TABLE IF NOT EXISTS contests"
                "(name TEXT NOT NULL UNIQUE,"
                "type TEXT NOT NULL,"
                "filename TEXT NOT NULL,"
                "num_judges integer,"
                "judges TEXT)")

    # table for judges
    # projects are separated by ","
    cur.execute("CREATE TABLE IF NOT EXISTS judges"
                "(username TEXT NOT NULL UNIQUE,"
                "contest TEST NOT NULL,"
                "company TEXT,"
                "real_name TEXT,"
                "projects TEXT,"
                "UNIQUE(username, contest))")

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

    # add admin user
    add_row_to_table("users", ("admin", "password", 2))

    # add test data
    # test row as dict
    add_row_to_table("users", {"username": "judge1",
                               "password": "password",
                               "access_level": 1})

    # test row as series
    add_row_to_table("judges", {"username": "judge1",
                                "contest": "contest1",
                                "company": "philsmart",
                                "real_name": "phil",
                                "projects": "test1,test2"})

    create_projects_table("contest1")

    add_row_to_table("projectscontest1", ("test1", "worst",
                                          "jinginllc", "mrjingin",
                                          "profjingin", "jg 115",
                                          "jin, gin", "JG 4",
                                          "judge1"))

    add_row_to_table("projectscontest1", ("test2", "best",
                                          "jinginllc", "mrjingin",
                                          "profjingin", "jg 115",
                                          "jin, gin", "JG 4",
                                          "judge1"))

    add_row_to_table("projectscontest1", ("test3", "ours",
                                          "jinginllc", "mrjingin",
                                          "profjingin", "jg 115",
                                          "jin, gin", "JG 4",
                                          "judge1"))


def add_row_to_table(table, row):
    # XXX: do we really want "OR IGNORE" in the sql statements?

    if isinstance(row, dict):  # convert dict to series
        row = pd.Series(row)

    if isinstance(row, pd.Series):  # handles dict and series
        keys = row.keys()
        vals = list(row)
        exp = ("INSERT OR IGNORE INTO %s (%s) VALUES (%s)" %
               (table,
                ",".join(keys),
                ",".join("?" * len(vals))))
    else:  # intended for 1-d sequences
        vals = list(row)
        exp = ("INSERT OR IGNORE INTO %s VALUES (%s)" %
               (table,
                ",".join("?" * len(vals))))

    conn = sql.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(exp, vals)
    conn.commit()
    conn.close()


def create_projects_table(contest_name):
    conn = sql.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS projects%s" % str(contest_name) +
                "(id TEXT NOT NULL UNIQUE,"
                "title TEXT NOT NULL UNIQUE,"
                "company TEXT,"
                "sponsor TEXT,"
                "instructor TEXT,"
                "course TEXT,"
                "students TEXT,"
                "location TEXT,"
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


def get_contest_for_judge(judge):
    df = get_table("judges")

    return df[df["username"] == judge]["contest"].item()


def get_projects_for_judge(judge):
    """Get a list of the projects assigned to judge."""
    df = get_table("judges")

    if not df.empty:
        return df[df["username"] == judge]["projects"].item().split(",")
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
