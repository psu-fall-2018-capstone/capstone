# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello():
    N = 5
    name = request.args.get("here0", "")
    return render_template("hello.html", name=name, N=N)
