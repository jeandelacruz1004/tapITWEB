import requests, json

from flask import Flask, render_template, session, redirect, request, url_for
from app.forms import *

tap = Flask(__name__)


@tap.route("/")
@tap.route("/landing")
def welcome():
    if "app" in session:
        return redirect("home")

    return render_template("index.html")
@tap.route("/admin")
def admin():
    return render_template("admin.html")

@tap.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@tap.route("/login", methods=["GET","POST"])
def login():
    if "app" in session:
        return redirect("home")

    return render_template("login.html")


@tap.route("/signup", methods=["GET", "POST"])
def signup():
    if "app" in session:
        return redirect("home")

    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        rfID = request.form.get("rfID")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        signup = requests.post("http://127.0.0.1:5000/user/",
                               data={'public_id': first_name + " " + last_name,
                                     'username': username,
                                     'email': email,
                                     'rfID': rfID,
                                     'password': password})
        return redirect(url_for('login'))

    return render_template("signup.html")
