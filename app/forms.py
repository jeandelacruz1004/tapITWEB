from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email, NumberRange, EqualTo


class Login(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    remember = BooleanField("Remember Password")

    submit = SubmitField("Log In")


class SignUp(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    rfID = StringField("RFID", validators=[Optional()])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=50)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')
