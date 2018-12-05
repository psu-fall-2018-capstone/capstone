# -*- coding: utf-8 -*-
from functools import reduce
from flask import Blueprint, render_template, request, session
import capstone.utils as utils

judge_api = Blueprint("judge", __name__)


@judge_api.before_request
@utils.required_access_level(1)
def before_request():
    """protects all judge endpoints"""
    pass


@judge_api.route("/", methods=["GET", "POST"])
@judge_api.route("/dashboard", methods=["GET", "POST"])
def judge_voting_dashboard():
    projects = utils.get_projects_for_judge(session["username"])
    proj_df = utils.get_table("projects" + session["contest"])

    selection = proj_df["id"].copy()
    selection[:] = False

    for project in projects:
        selection |= (proj_df["id"] == project)

    projects = proj_df[selection]

    return render_template("judge_voting_dashboard.html",
                           title="Judge Voting Dashboard",
                           judge_projects=projects)


@judge_api.route("/voting", methods=["GET", "POST"])
@judge_api.route("/voting/<project>", methods=["GET", "POST"])
def judge_project_voting(project=None):
    if project is None:
        project = request.args.get("project", None)
        if project is None:
            raise RuntimeError("you shouuldn't bEE hEEREEEEE !!!")

    questions = utils.project_questions()

    # gets the scores from each question and saves to a string
    # TODO: save to session or database
    if request.method == "POST":
        scores = ""

        for i in range(len(questions)):
            score = request.form.get("q" + str(i + 1), "*")
            scores += score + ", "

    return render_template("judge_project_voting.html",
                           title="Judge Project voting",
                           projectSelection=project,
                           judgeQuestions=questions)
