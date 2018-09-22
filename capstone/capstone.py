# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def hello(N=5):
    name = [request.form["data" + str(i)] for i in range(N)]
    return render_template("hello.html", name="\n".join(name), N=N)
