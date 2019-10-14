from flask import Flask, render_template

tap = Flask(__name__)


@tap.route("/")
@tap.route("/landing")
def hello():

    return render_template("index.html")
