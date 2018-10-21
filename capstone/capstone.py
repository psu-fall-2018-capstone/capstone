# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from capstone.admin import admin_api
from capstone.judge import judge_api

app = Flask(__name__)

app.register_blueprint(admin_api, url_prefix="/admin")
app.register_blueprint(judge_api, url_prefix="/judge")


@app.route("/", methods=["GET", "POST"])
def hello():
    return "Hello world!"
