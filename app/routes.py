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
        print(first_name, last_name, username)

        signup = requests.post("http://127.0.0.1:5000/user/",
                               data={'public_id': first_name + " " + last_name,
                                     'username': username,
                                     'email': email,
                                     'rfID': rfID,
                                     'password': password})
        return redirect(url_for('welcome'))

    return render_template("signup.html")

@tap.route("/login", methods=["GET", "POST"])
def login():
    if "app" in session:
        return redirect("home")

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        login = requests.post("http://127.0.0.1:5000/auth/login",
                               data={'email': email,
                                    'password': password})
        if login.status_code == 200:
            return redirect(url_for('signup'))
        else:
            return redirect(url_for("login"))


    return render_template("login.html")

#@tap.route("/login", methods=['POST','GET'])
#def login():
#    if "app" in session:
#        return redirect("home")

#    print('wa kasulod')
#    if request.method == "POST":
        
#        print('sulod')
#        email = request.form.get("email") 
#        password = request.form.get("password")

        # if check_user.status_code == 200:
#       if request.form.get("username") == ("admin"):
#            print('sulod admin')
#            login = requests.post("http://127.0.0.1:5000/auth/login",form={"email":email, "password":password})
#            print(login.status_code)
#            print("admin")
#            if login.status_code == 400:
#                print("Email or password is incorrect")  
                
#            else: 
#                return redirect(url_for('signup'))

#       elif request.form.get("admin") == ("false"):
#            print('sulod useeer')
#            login = requests.post("http://127.0.0.1:5000/auth/login",form={"email":email, "password":password})
#            print(login.status_code)
#            print("custom")
#            if response.status_code == 400:
#                print("Email or password is incorrect")
                
#            else:
#                return redirect(url_for('welcome'))
#                print("user not found")

#    return render_template('login.html')
