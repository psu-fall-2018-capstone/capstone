# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request

judge_api = Blueprint("judge", __name__)


@judge_api.route("/", methods=["GET", "POST"])
@judge_api.route("/dashboard", methods=["GET", "POST"])
def judge_voting_dashboard():
    judgeProjectList = ["Project1",
                        "Project2",
                        "Project3",
                        "Project4",
                        "Project5"]
    if request.method == 'POST':
        judgeProjectSelection = request.form['projectSelection']
        print(judgeProjectSelection)
        return render_template("judge_project_voting.html",
                               title="Judge Project voting",
                               projectSelection=judgeProjectSelection)
    return render_template("judge_voting_dashboard.html",
                           title="Judge Voting Dashboard",
                           judgeProjectArray=judgeProjectList)


@judge_api.route("/voting", methods=["GET", "POST"])
@judge_api.route("/voting/<project>", methods=["GET", "POST"])
def judge_project_voting(project=None):
    if project is None:
        project = request.args.get("project", None)
        if project is None:
            raise RuntimeError("you shouuldn't bEE hEEREEEEE !!!")
    return render_template("judge_project_voting.html",
                           title="Judge Project voting",
                           projectSelection=project)
