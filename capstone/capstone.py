# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from capstone.admin import admin_api

app = Flask(__name__)

app.register_blueprint(admin_api, url_prefix="/admin")


@app.route("/", methods=["GET", "POST"])
def hello():
    return "Hello world!"


@app.route("/judge_voting_dashboard", methods=["GET", "POST"])
def judge_voting_dashboard():
    judgeProjectList = ["Project1",
                        "Project2",
                        "Project3",
                        "Project4",
                        "Project5"]
    if request.method == 'POST':
        judgeProjectSelection = request.form['projectSelection']
        print(judgeProjectSelection)
        return "Test"
    return render_template("judge_voting_dashboard.html",
                           title="Judge Voting Dashboard",
                           judgeProjectArray=judgeProjectList)
