# -*- coding: utf-8 -*-
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
    judgeProjectList = utils.get_projects_for_judge(session["username"])

    return render_template("judge_voting_dashboard.html",
                           title="Judge Voting Dashboard",
                           judgeProjectArray=judgeProjectList)


PROJECT_QUESTIONS = [
    ("Did the team approach the problem in a way that is consistent with the "
     "disciplinary expertise of its members?"),
    ("Was appropriate modeling, analysis, and/or testing used to help identify"
     " and refine solutions?"),
    "Was the team creative in their solution and/or approach to the problem?",
    ("Does the project solution directly address the customer's stated "
     "objectives (is the solution appropriate)?"),
    ("Does the project solution meet/exceed customer's expectations (is the "
     "customer satisfied)?"),
    ("Did the team demonstrate improvements in product/process quality or cost"
     "/time savings?"),
    ("Did the team acknowledge and stay within design constraints (e.g., "
     "budget, schedule, cost)?"),
    ("Did the oral presentation clearly convey the necessary background, "
     "approach, results, and recommendations?"),
    ("Did the team's display (poster, simulation, prototype, etc.) clearly "
     "describe the technical project and solution?"),
    ("Other noteworthy aspects not covered above that add value to the project"
     " quality and/or completeness<br/>(e.g., level of difficulty of project, new "
     "technology and/or innovative process or product, cool, etc.)?")
]


@judge_api.route("/voting", methods=["GET", "POST"])
@judge_api.route("/voting/<project>", methods=["GET", "POST"])
def judge_project_voting(project=None):
    if project is None:
        project = request.args.get("project", None)
        if project is None:
            raise RuntimeError("you shouuldn't bEE hEEREEEEE !!!")

    questions = PROJECT_QUESTIONS

    # gets the scores from each question and saves to a string
    # TODO: save to session or database
    if request.method == "POST":
        scores = ""

        for i in range(len(questions)):
            score = request.form.get("q" + str(i + 1), "*")
            scores += score + ", "

        print(scores)

    return render_template("judge_project_voting.html",
                           title="Judge Project voting",
                           projectSelection=project,
                           judgeQuestions=questions)
