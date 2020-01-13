import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_babelex import Babel

key = secrets.token_hex(16)

app = Flask(__name__)
app.config['SECRET_KEY'] = key
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/tapITWEB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USERNAME'] = 'mail@tapit.com'
# app.config['MAIL_PASSWORD'] = 'password'
# app.config['MAIL_DEFAULT_SENDER'] = '"TapIT" <noreply@tapit.com>'
#
# app.config['USER_APP_NAME'] = 'Flask-User Basic App'
# app.config['USER_ENABLE_EMAIL'] = True
# app.config['USER_ENABLE_USERNAME'] = False
# app.config['USER_EMAIL_SENDER_NAME'] = ['USER_APP_NAME']
# app.config['USER_EMAIL_SENDER_EMAIL'] = 'noreply@tapit.com'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# babel = Babel(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from tapit import routes
