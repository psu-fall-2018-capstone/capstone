# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

admin_api = Blueprint("admin", __name__)


@admin_api.route("/admindashboard", methods=["GET", "POST"])
def admindashboard():
    return render_template("admindashboard.html", title="Admin Dashboard")


@admin_api.route("/adminjudgesetup", methods=["GET", "POST"])
def adminjudgesetup():  # this page does the file upload
    if request.method == 'POST':
        return render_template("adminjudgesetup.html",
                               title="File Upload",
                               submitted=True)
    else:
        return render_template("adminjudgesetup.html",
                               title="File Upload",
                               submitted=False)


@admin_api.route("/adminjudgeassignment", methods=["GET", "POST"])
def judgeassignment():
    exclusions = 1
    judgeArrayList = ["Phillip",
                      "Marko",
                      "Tyler"]  # this will need to be populated dynamically
    projectArrayList = ["CapstoneRedesign",
                        "AnotherProject",
                        "AnotherProject2"]
    if request.method == 'POST':
        exclusions = request.form['exclusions']
        return render_template("adminjudgeassignment.html",
                               title="Judge Assignment",
                               numExclusions=exclusions,
                               judgeArray=judgeArrayList,
                               projectArray=projectArrayList)

    return render_template("adminjudgeassignment.html",
                           title="Judge Assignment",
                           numExclusions=exclusions,
                           judgeArray=judgeArrayList,
                           projectArray=projectArrayList)


@admin_api.route("/adminresults", methods=["GET", "POST"])
def adminresults():
    return render_template("adminresults.html", title="Admin Results")


@admin_api.route("/admintracking", methods=["GET", "POST"])
def admintracking():
    return render_template("admintracking.html", title="Admin Tracking")


@admin_api.route("/adminpopularityresults", methods=["GET", "POST"])
def adminpopularityresults():
    return "You are on the adminpopularityresults"


@admin_api.route("/adminpopularitytracking", methods=["GET", "POST"])
def adminpopularitytracking():
    return "You are on the adminpopularitytracking"


@admin_api.route("/adminposterresults", methods=["GET", "POST"])
def adminposterresults():
    return "You are on the adminposterresults"


@admin_api.route("/adminpostertracking", methods=["GET", "POST"])
def adminpostertracking():
    return "You are on the adminpostertracking"


@admin_api.route("/adminprojectresults", methods=["GET", "POST"])
def adminprojectresults():
    return "You are on the adminprojectresults"


@admin_api.route("/adminprojecttracking", methods=["GET", "POST"])
def adminprojecttracking():
    return "You are on the adminprojecttracking"
