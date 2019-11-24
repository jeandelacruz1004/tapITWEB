import os, secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
# from flask_user import roles_required

from tapit import app, db, bcrypt
from tapit.forms import LoginForm, RegistrationForm, UpdateAccountForm, NewEventForm
from tapit.models import User, Event
# from tapit.decorator import admin_login_required


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('landing'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("index.html", title='Welcome', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img/profile', picture_fn)
    form_picture.save(picture_path)

    # output_size = (600, 600)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)

    return picture_fn


@app.route("/landing", methods=['GET','POST'])
@login_required
def landing():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.rfID = form.rfID.data
        current_user.contact = form.contact.data
        db.session.commit()
        flash('Account has been updated!', 'success')
        return redirect(url_for('landing'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.rfID.data = current_user.rfID
        form.contact.data = current_user.contact
        image_file = url_for('static', filename='img/profile/' + current_user.image_file)
    return render_template("landing.html", title=current_user.username, image_file=image_file, form=form)


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template("signup.html", title='Create Account', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('landing'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template("login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/events/")
@login_required
# @admin_login_required
def disp_events():
    image_file = url_for('static', filename='img/banner' + Event.banner)
    events = Event.query.all()
    return render_template('events.html', title='Events', events=events, image_file=image_file)


@app.route("/events/<int:id>")
@login_required
# @admin_login_required
def disp_event_details(id):
    image_file = url_for('static', filename='img/banner' + Event.banner)
    events = Event.query.filter_by(id=id).first()
    return render_template('events.html', title='Events', events=events, image_file=image_file)


@app.route("/events/create", methods=['GET', 'POST'])
@login_required
def new_event():
    if current_user.is_admin is True or current_user.is_faculty is True:
        image_file = url_for('static', filename='img/banner' + Event.banner)
        form = NewEventForm()
        if form.validate_on_submit():
            newevent = Event(user_id=current_user.id,
                             title=form.title.data,
                             start_time=form.start_time.data,
                             end_time=form.end_time.data,
                             details=form.details.data
                             )
            if form.image_file.data:
                picture_file = save_picture(form.image_file.data)
                newevent.image_file = picture_file
            db.session.add(newevent)
            db.session.commit()
            flash(f'Event Successfully Created!', 'success')
            return redirect(url_for('landing'))
    else:
        flash(f'Contact a Faculty in order to create events.', 'warning')
        return redirect(url_for('landing'))

    return render_template('addevent.html', title='Add Event', form=form, image_file=image_file)


@app.route("/events/data/", methods=['GET', 'POST'])
@login_required
def manage_events():
    users = User.query.all()
    events = Event.query.all()
    if current_user.is_admin is not True:
        flash(f'You should be an administrator to access this page', 'warning')
        return redirect(url_for('landing'))
    return render_template('eventdata.html', title='Manage Events', events=events, users=users)


@app.route("/events/data/<int:id>", methods=['GET', 'POST'])
@login_required
def edit_events(id):
    if current_user.is_admin is not True:
        flash(f'You should be an administrator to access this page', 'warning')
        return redirect(url_for('landing'))
    users = User.query.all()
    events = Event.query.filter_by(id=id).first()
    return render_template('eventdata.html', title='Manage Events', events=events, users=users)


@app.route("/users/data/", methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.is_admin is not True:
        flash(f'You should be an administrator to access this page', 'warning')
        return redirect(url_for('landing'))
    users = User.query.all()
    form = UpdateAccountForm()
    return render_template('userdata.html', title='Manage Users', users=users, form=form)


@app.route("/users/data/<int:id>/edit", methods=['GET', 'POST'])
@login_required
def update_users(id):
    if current_user.is_admin is not True:
        flash(f'You should be an administrator to access this page', 'warning')
        return redirect(url_for('landing'))
    else:
        users = User.query.filter_by(id=id).first()
        form = UpdateAccountForm()
        if form.validate_on_submit():
            if form.image_file.data:
                picture_file = save_picture(form.image_file.data)
                users.image_file = picture_file
            users.first_name = form.first_name.data
            users.last_name = form.last_name.data
            users.username = form.username.data
            users.email = form.email.data
            users.rfID = form.rfID.data
            users.contact = form.contact.data
            db.session.commit()
            flash('Account has been updated!', 'success')
            return redirect(url_for('landing'))
        elif request.method == 'GET':
            form.first_name.data = users.first_name
            form.last_name.data = users.last_name
            form.username.data = users.username
            form.email.data = users.email
            form.rfID.data = users.rfID
            form.contact.data = users.contact
        image_file = url_for('static', filename='img/profile/' + users.image_file)
    return render_template('userdata.html', title='Manage Users', users=users, form=form, image_file=image_file)


