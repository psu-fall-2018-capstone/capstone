# -*- coding: utf-8 -*-
import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
from capstone.utils import required_access_level

admin_api = Blueprint("admin", __name__)

ALLOWED_EXTENSIONS = set(["xlsx"])


@admin_api.before_request
@required_access_level(2)
def before_request():
    """protects all admin endpoints"""
    pass


@admin_api.route("/", methods=["GET", "POST"])
@admin_api.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("admin_dashboard.html", title="Admin Dashboard")


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_api.route("/judge_setup", methods=["GET", "POST"])
def judge_setup():  # this page does the file upload
    if request.method == 'POST':
        file = request.files["myFile"]

        if file.filename == '':
            return "no file selected"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)  # save to specific folder

            return render_template("admin_judge_setup.html",
                                   title="File Upload",
                                   submitted=True)
        else:
            return "upload failed"
    else:
        return render_template("admin_judge_setup.html",
                               title="File Upload",
                               submitted=False)


@admin_api.route("/judge_assignment", methods=["GET", "POST"])
def judge_assignment():
    exclusions = 1
    judgeArrayList = ["Phillip",
                      "Marko",
                      "Tyler"]  # this will need to be populated dynamically
    projectArrayList = ["CapstoneRedesign",
                        "AnotherProject",
                        "AnotherProject2"]
    if request.method == 'POST':
        exclusions = request.form['exclusions']
        return render_template("admin_judge_assignment.html",
                               title="Judge Assignment",
                               numExclusions=exclusions,
                               judgeArray=judgeArrayList,
                               projectArray=projectArrayList)

    return render_template("admin_judge_assignment.html",
                           title="Judge Assignment",
                           numExclusions=exclusions,
                           judgeArray=judgeArrayList,
                           projectArray=projectArrayList)


@admin_api.route("/results", methods=["GET", "POST"])
def results():
    return render_template("admin_results.html", title="Admin Results")


@admin_api.route("/tracking", methods=["GET", "POST"])
def tracking():
    return render_template("admin_tracking.html", title="Admin Tracking")


@admin_api.route("/results/popularity", methods=["GET", "POST"])
def results_popularity():
    return "You are on the admin_popularity_results"


@admin_api.route("/tracking/popularity", methods=["GET", "POST"])
def tracking_popularity():
    return "You are on the admin_popularity_tracking"


@admin_api.route("/results/poster", methods=["GET", "POST"])
def results_poster():
    return "You are on the admin_poster_results"


@admin_api.route("/tracking/poster", methods=["GET", "POST"])
def tracking_poster():
    return "You are on the admin_poster_tracking"


@admin_api.route("/results/project", methods=["GET", "POST"])
def results_project():
    return "You are on the admin_project_results"


@admin_api.route("/tracking/project", methods=["GET", "POST"])
def tracking_project():
    return "You are on the admin_project_tracking"
