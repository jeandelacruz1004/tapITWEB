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
        return redirect(url_for('welcome'))

    return render_template("signup.html")

#User
@tap.route("/dashboardUser", methods=["GET", "POST"])
def dashboardUser():
    if "app" in session:
        return redirect("dashboardUser")

    return render_template("dashboardUser.html")


#admin
@tap.route("/admin")
def admin():
    return render_template("admin.html")

@tap.route("/adminprof")
def adminprof():
    return render_template("adminprofile.html")
@tap.route("/logout")
def logout():
    print('sulod')
    session.pop('username', None)
    print("beeplop")
    return render_template("index.html")

@tap.route("/table")
def table():
    return render_template("table.html")

@tap.route("/events")
def events():
    return render_template("events.html")
