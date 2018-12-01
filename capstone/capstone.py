# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3 as sql
import capstone.helpers as helper
from capstone.admin import admin_api
from capstone.judge import judge_api

app = Flask(__name__)
app.secret_key = 'test'

app.register_blueprint(admin_api, url_prefix="/admin")
app.register_blueprint(judge_api, url_prefix="/judge")


@app.before_first_request
def initialize():
    helper.init_db()


@app.route("/")
@app.route("/home")
def home():
    if "user" in session:
        access_level = helper.get_user_access_level(session["user"])
        if access_level == 2:
            return redirect(url_for("admin.dashboard"))
        elif access_level == 1:
            return redirect(url_for("judge.dashboard"))

        return "not a user"

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user" not in session:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            check = helper.validate(username, password)

            if check:
                session["user"] = username
                return redirect(url_for("home"))
            else:
                return "wrong password"
        return render_template("login.html")
    return redirect(url_for("home"))

    
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

