# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
from capstone.admin import admin_api
from capstone.judge import judge_api
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'test'

app.register_blueprint(admin_api, url_prefix="/admin")
app.register_blueprint(judge_api, url_prefix="/judge")

conn = sql.connect("database.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS users")
cur.execute('''CREATE TABLE users 
    (username TEXT NOT NULL, 
     password TEXT NOT NULL)''')
cur.execute("INSERT INTO users VALUES (?,?)", ("admin", "password"))
conn.commit()
conn.close()


# @app.route("/", methods=["GET", "POST"])
# def hello():
#     return "Hello world!"


@app.route("/")
@app.route("/home")
def home():
    if "username" in session:
        if session["username"] == "admin":
            return redirect(url_for("admin.dashboard"))

        return "notadmin"

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "username" not in session:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            check = validate(username, password)

            if check:
                session["username"] = username
                return redirect(url_for("home"))
            else:
                return "wrong password"

        return render_template("login.html")

    return redirect(url_for("home"))

    
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


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
