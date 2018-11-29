# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
from capstone.admin import admin_api
from capstone.judge import judge_api

app = Flask(__name__)
app.secret_key = 'test'

app.register_blueprint(admin_api, url_prefix="/admin")
app.register_blueprint(judge_api, url_prefix="/judge")


@app.before_first_request
def init_db():
    conn = sql.connect("database.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute('''CREATE TABLE users 
        (username TEXT NOT NULL, 
         password TEXT NOT NULL)''')
    cur.execute("INSERT INTO users VALUES (?,?)", ("admin", "password"))
    conn.commit()
    conn.close()


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
