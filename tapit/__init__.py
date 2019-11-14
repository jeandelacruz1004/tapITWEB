import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

key = secrets.token_hex(16)


app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:regards@localhost:5432/Secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from tapit import routes
