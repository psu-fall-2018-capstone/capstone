# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello(N=5):
    return "Hello world!"
    #name = [request.form["data" + str(i)] for i in range(N)]
    #return render_template("hello.html", name="\n".join(name), N=N)

@app.route("/admindashboard", methods=["GET", "POST"])
def admindashboard():
    return "You are on the admindashboard"

@app.route("/adminjudgeassignment", methods=["GET", "POST"])
def judgeassignment():
    return "You are on the adminjudgeassignment"

@app.route("/adminjudgesetup", methods=["GET", "POST"])
def adminjudgesetup():
    return "You are on the adminjudgesetup"

@app.route("/adminpopularityresults", methods=["GET", "POST"])
def adminpopularityresults():
    return "You are on the adminpopularityresults"

@app.route("/adminpopularitytracking", methods=["GET", "POST"])
def adminpopularitytracking():
    return "You are on the adminpopularitytracking"

@app.route("/adminposterresults", methods=["GET", "POST"])
def adminposterresults():
    return "You are on the adminposterresults"

@app.route("/adminpostertracking", methods=["GET", "POST"])
def adminpostertracking():
    return "You are on the adminpostertracking"

@app.route("/adminprojectresults", methods=["GET", "POST"])
def adminprojectresults():
    return "You are on the adminprojectresults"

@app.route("/adminprojecttracking", methods=["GET", "POST"])
def adminprojecttracking():
    return "You are on the adminprojecttracking"

if __name__ == "__main__":
    app.run()
