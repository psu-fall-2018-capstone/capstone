# -*- coding: utf-8 -*-
import os
from flask import Blueprint, render_template, request
from werkzeug.utils import secure_filename
import capstone.utils as utils

admin_api = Blueprint("admin", __name__)


@admin_api.before_request
@utils.required_access_level(2)
def before_request():
    """protects all admin endpoints"""
    pass


@admin_api.route("/", methods=["GET", "POST"])
@admin_api.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    return render_template("admin_dashboard.html", title="Admin Dashboard")


@admin_api.route("/contest_setup", methods=["GET", "POST"])
def contest_setup():
    if request.method == "POST":
        if "contest-name" in request.form:
            contest_name = request.form["contest-name"]

        if "contest-type" in request.form:
            contest_type = request.form["contest-type"]

        if "contest-file" in request.files:
            file = request.files["contest-file"]

            if file and utils.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(utils.UPLOAD_FOLDER, filename))

    # TODO: only allow submission when all 3 inputs have been set
    return render_template("admin_contest_setup.html",
                           contest_types=utils.CONTEST_TYPES)


@admin_api.route("/judge_assignment", methods=["GET", "POST"])
def judge_assignment():
    exclusions = 1
    judgeArrayList = ["Phillip",
                      "Marko",
                      "Tyler"]  # this will need to be populated dynamically
    projectArrayList = ["CapstoneRedesign",
                        "AnotherProject",
                        "AnotherProject2"]
    if request.method == "POST":
        # exclusions = request.form["exclusions"] this does nothing right now
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


@admin_api.route("/judge_add", methods=["GET", "POST"])
def judge_add():
    displayJudgeBoxes = False
    judge_Num = 0
    # this array needs to be populated dynamically
    sponsorArrayList = ["sponsor1",
                        "sponsor2",
                        "sponsor3"]
    if request.method == "POST":
        displayJudgeBoxes = True
        judge_Num = int(request.form["judgenum"])
        return render_template("/admin_judge_add.html", title="Add Judges",
                               displayBoxes=displayJudgeBoxes,
                               numJudges=judge_Num,
                               sponsorArray=sponsorArrayList)

    return render_template("/admin_judge_add.html", title="Add Judges",
                           displayBoxes=displayJudgeBoxes,
                           numJudges=judge_Num,
                           sponsorArray=sponsorArrayList)


# page for selecting which projects should be judged based on their poster
@admin_api.route("/poster_project_select", methods=["GET", "POST"])
def poster_project_select():
    # this needs to be populated dynamically
    projectArrayList = ["project1",
                        "project2",
                        "project3"]

    numProjectsToJudge = 0
    stage = 0
    # stage 0: input num projects | stage 1: select Projects to be judged

    selectedProjectsArrayList = [] # fill this in the POST

    if request.method == "POST":
        stage = int(request.form["stage"])
        if stage == 0:
            numProjectsToJudge = int(request.form["proj_num"])
            return render_template("/admin_poster_project_select.html",
                                   title="Poster Project Select",
                                   numProjects=numProjectsToJudge,
                                   projectArray=projectArrayList)
        else:
            # TODO: fill the selectedProjectsArrayList with selection
            return "Projects selected successfully!"
    return render_template("/admin_poster_project_select.html",
                           title="Poster Project Select",
                           numProjects=numProjectsToJudge,
                           projectArray=projectArrayList)


# page for selecting projects for contest
@admin_api.route("/technical_project_select", methods=["GET", "POST"])
def technical_project_select():
    # this needs to be populated dynamically
    projectArrayList = ["project1",
                        "project2",
                        "project3"]

    numProjectsToJudge = 0
    stage = 0
    # stage 0: input num projects | stage 1: select Projects to be judged

    selectedProjectsArrayList = [] # fill this in the POST

    if request.method == "POST":
        stage = int(request.form["stage"])
        if stage == 0:
            numProjectsToJudge = int(request.form["proj_num"])
            return render_template("/admin_technical_project_select.html",
                                   title="Technical Project Select",
                                   numProjects=numProjectsToJudge,
                                   projectArray=projectArrayList)
        else:
            # TODO: fill the selectedProjectsArrayList with selection
            return "Projects selected successfully!"
    return render_template("/admin_technical_project_select.html",
                           title="Technical Project Select",
                           numProjects=numProjectsToJudge,
                           projectArray=projectArrayList)


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
