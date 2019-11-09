import requests, json

from flask_mail import Message
from flask import Flask, render_template, session, redirect, request, url_for, flash
from app.forms import *

tap = Flask(__name__)


@tap.route("/")
@tap.route("/landing")
def welcome():
    if "app" in session:
        return redirect("home")

    return render_template("index.html")

#Routing for Registration
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

        signup = requests.post("http://127.0.0.1:5000//auth/user/",
                               data={'public_id': first_name + " " + last_name,
                                     'username': username,
                                     'email': email,
                                     'rfID': rfID,
                                     'password': password})
        return redirect(url_for('welcome'))

    return render_template("signup.html")
#Routing for Login 
@tap.route("/login", methods=['POST','GET'])
def login():

    if request.method == "POST":
        print("yey kasulod ko ")
        email = request.form["email"]
        password = request.form["password"]
 
        login = requests.post("http://127.0.0.1:5000/auth/login",data={'email': email,'password': password})

        if login.status_code == 200:
            if email == "admin@gmail.com":
                print(login.status_code)
                return redirect(url_for('admin'))   
            else: 
                return render_template("userdashboard.html")
    return render_template("login.html")
#Routing for Admin
@tap.route("/admin",methods=["GET","POST"])
def admin():
    return render_template("admin.html")

@tap.route("/adminprof",methods=["GET","POST"])
def adminprof():
    return render_template("adminprofile.html")
@tap.route("/logout",methods=["GET","POST"])
def logout():
    print('sulod')
    session.pop('username', None)
    print("beeplop")
    return render_template("index.html")

@tap.route("/table",methods=["GET","POST"])
def table():
    return render_template("table.html")



@tap.route("/events",methods=["GET","POST"])
def adddevents():
    print("yey nakasulod ko")
    if request.method == "POST":
        print ("nakasulod na pud ko pag post")

        eventName = request.form['eventName ']
        dateCreated = request.form['dateCreated']
        eventDate = request.form['eventDate']
        eventStartTime = request.form['eventStartTime']
        eventEndTime = request.form['eventEndTime']
        eventDesciption = request.form['eventDesciption']
        location = request.form['location']
        
        
        response = requests.post("http://127.0.0.1:5000/events/",
        json={"eventName":eventName, "dateCreated":dateCreated, "eventStartTime":eventStartTime, " eventEndTime": eventEndTime,"eventDesciption":eventDesciption,  "location":location}, )
        print(response.text)
    

        
    return render_template("events.html")

#Routing for User
@tap.route("/userdashboard", methods=["GET", "POST"])
def dashboardUser():
    if "app" in session:
        return redirect("userdashboard")

    return render_template("userdashboard.html")

@tap.route("/usersettings", methods=["GET", "POST"])
def usersettings():
    if "app" in session:
        return redirect("usersettings")

    return render_template("usersettings.html")

@tap.route("/userprof")
def userprof():
    return render_template("userprofile.html")
   
  
