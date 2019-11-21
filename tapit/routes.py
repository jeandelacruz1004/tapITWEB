import os, secrets
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
# from flask_user import roles_required

from tapit import app, db, bcrypt
from tapit.forms import LoginForm, RegistrationForm, UpdateAccountForm, NewEventForm, forms
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

@app.route("/attendance")
def attendance():
    
    return render_template("attendance.html")


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')



@app.route('/addparticipant',methods=['POST','GET'])
def addparticipant():
    if current_user.is_authenticated:
        return redirect(url_for('addparticipant'))
    form = forms(request.method)
    if form.validate_on_submit():
        user = User(
            idnumber=form.idnumber.data,
            firstname=form.firstname.data,
                    lastname=form.lastname.data,
                    gender=form.gender.data,
                    yearlevel=form.yearlevel.data,
                    course_id=form.course_id.data)
        print(user)
        db.session.add(user)
        db.session.commit()
        return redirect('/attendance')
    return render_template('attendance.html',form=form , title='Add')

    
events = [
    {
        'title': 'Palakasan MMXX',
        'start_time': 'April 17, 2020',
        'end_time': 'April 24, 2020',
        'details': 'Lorem ipsum whatever',
        'date_created': 'April 1, 2020',
    },
    {
        'title': 'Intellectual Property Foundation: Patents, Copyrights & Other IPs',
        'start_time': 'Nov 20, 2019 8:30AM',
        'end_time': 'Nov 20, 2019 12:00NN',
        'details': 'CED Amphitheater',
        'date_created': 'Nov 17, 2019',
    },
    {
        'title': 'Palakasan MMXX',
        'start_time': 'April 17, 2020',
        'end_time': 'April 24, 2020',
        'details': 'Lorem ipsum whatever',
        'date_created': 'April 1, 2020',
    },
    {
        'title': 'Intellectual Property Foundation: Patents, Copyrights & Other IPs',
        'start_time': 'Nov 20, 2019 8:30AM',
        'end_time': 'Nov 20, 2019 12:00NN',
        'details': 'CED Amphitheater',
        'date_created': 'Nov 17, 2019',
    },
    {
        'title': 'Palakasan MMXX',
        'start_time': 'April 17, 2020',
        'end_time': 'April 24, 2020',
        'details': 'Lorem ipsum whatever',
        'date_created': 'April 1, 2020',
    },
    {
        'title': 'Intellectual Property Foundation: Patents, Copyrights & Other IPs',
        'start_time': 'Nov 20, 2019 8:30AM',
        'end_time': 'Nov 20, 2019 12:00NN',
        'details': 'CED Amphitheater',
        'date_created': 'Nov 17, 2019',
    },
]


@app.route("/events")
@login_required
# @admin_login_required
def disp_events():
    image_file = url_for('static', filename='img/banner' + Event.banner)
    users = User.query.filter_by(id=id).first
    events = Event.query.all()
    return render_template('events.html', title='Events', events=events, users=users, image_file=image_file)


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


@app.route("/calendar")
def calendar():
    return render_template('calendar.html')


@app.route("/json")
def json():
    return render_template('json.html')


@app.route('/data')
def return_data():
    start_date = request.args.get('start', '')
    end_date = request.args.get('end', '')


    with open("tapit/events.json", "r") as input_data:
       
        return input_data.read()
@app.route("/events/data", methods=['GET', 'POST'])
@login_required
def manage_events():
    users = User.query.all()
    events = Event.query.all()
    if current_user.is_admin is not True:
        flash(f'You should be an administrator to access this page', 'warning')
        return redirect(url_for('landing'))
    return render_template('eventdata.html', title='Manage Events', events=events, users=users)


@app.route("/events/requests", methods=['GET', 'POST'])
@login_required
def req_event():
    users = User.query.all()
    events = Event.query.all()
    if current_user.is_admin is not True:
        flash(f'You should be an administrator to access this page', 'warning')
        return redirect(url_for('landing'))
    return render_template('eventrequest.html', title='Events Requests', events=events, users=users)

@app.route("/event/<int:event_id>/join", methods=["GET", "POST"])
@login_required
def join_event(event_id):
    if request.method == 'POST':
        req = request.form['event_id']

        lookRow = db.session.query(join_rel_table).filter(join_rel_table.c.user_id==current_user.userId, join_rel_table.c.event_id==req).first()

        if lookRow is None:
            statement = join_rel_table.insert().values(user_id=current_user.userId, event_id=req)

            db.session.execute(statement)
            db.session.commit()
        
        return jsonify({'result' : 'success'})
