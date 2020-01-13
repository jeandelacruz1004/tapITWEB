from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField,IntegerField,HiddenField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, ValidationError
from tapit.models import User


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=18)])
    rfID = StringField('RFID', validators=[Optional()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please select another one.')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=18)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    rfID = StringField('RFID', validators=[Optional()])
    contact = StringField('Contact Info', validators=[Optional()])
    image_file = FileField('Update User Photo', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    @staticmethod
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please select another one.')

    @staticmethod
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one.')
<<<<<<< HEAD
class NewEventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    details = StringField('Event Details', validators=[DataRequired()])
    image_file = FileField('Event Banner', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Create Event')
class AddVenueForm(FlaskForm):
    venue_name = StringField('Venue Name',validators=[DataRequired()])
    college = SelectField('College',id='college_id',validators=[DataRequired()], choices=[('1', 'MSU-IIT'), ('2', 'College of Engineering and Technology'), ('3', 'College of Science and Mathematics'), ('4', 'College of Education'), ('5', 'College of Arts and Social Sciences'), ('6', 'College of Business Administration and Accountancy'), ('7', 'College of Nursing'), ('8', 'College of Computer Studies'), ('9', 'Integrated Developmental School'), ('10', 'Premier Research Institute of Science and Mathematics')])
    capacity = IntegerField('Capacity',validators=[Optional()])
    details = StringField('Details', validators=[DataRequired()])
    equipment = StringField('Equipment',validators=[Optional()])
    image_file = FileField('Venue Banner', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Venue')

class UpdateVenueForm(FlaskForm):
    venue_name = StringField('Venue Name',validators=[DataRequired()])
    college = SelectField('College',id='college_id',validators=[DataRequired()], choices=[('1', 'MSU-IIT'), ('2', 'College of Engineering and Technology'), ('3', 'College of Science and Mathematics'), ('4', 'College of Education'), ('5', 'College of Arts and Social Sciences'), ('6', 'College of Business Administration and Accountancy'), ('7', 'College of Nursing'), ('8', 'College of Computer Studies'), ('9', 'Integrated Developmental School'), ('10', 'Premier Research Institute of Science and Mathematics')])
    capacity = IntegerField('Capacity',validators=[Optional()])
    details = StringField('Details', validators=[DataRequired()])
    equipment = StringField('Equipment',validators=[Optional()])
    image_file = FileField('Venue Banner', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    
=======


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class SearchForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class forms(FlaskForm):
    idnumber = StringField('ID Number', validators=[DataRequired(), Length(min=1, max=15)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=1, max=40)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=40)])
    gender = StringField('Gender', validators=[DataRequired(), Length(min=1, max=15)])
    yearlevel = StringField('Year Level', validators=[DataRequired(), Length(min=1, max=15)])
    course_id = StringField('Course ID', validators=[DataRequired(), Length(min=1, max=100)])
    course = StringField('Course Name', validators=[DataRequired(), Length(min=1, max=100)])
>>>>>>> Attendance
