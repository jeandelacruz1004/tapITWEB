from datetime import datetime
from tapit import db, login_manager, app
from flask_login import UserMixin
# from flask_user import UserManager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

join_rel_table = db.Table('join_rel_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')),
    db.Column('dateJoined', db.DateTime, nullable=False, default=datetime.utcnow)
)


COLLEGENAMES = {
    'MSU-IIT': 1,
    'College of Engineering and Technology': 2,
    'College of Science and Mathematics': 3,
    'College of Education': 4,
    'College of Arts and Social Science': 5,
    'College of Business Administration and Accountancy': 6,
    'College of Nursing': 7,
    'College of Computer Studies': 8,
    'Integrated Developmental School': 9,
    'PRISM': 10
}
COLLEGEID = {
    1: 'MSU-IIT',
    2: 'COET',
    3: 'CSM',
    4: 'CED',
    5: 'CASS',
    6: 'CBAA',
    7: 'CON',
    8: 'CCS',
    9: 'IDS',
    10: 'PRISM'
}

class User(db.Model, UserMixin):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    rfID = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(25), unique=True, nullable=False)
    last_name = db.Column(db.String(25), unique=False, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    contact = db.Column(db.String(20), unique=False, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), default='default.png', nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_student = db.Column(db.Boolean, default=True, nullable=False)
    is_faculty = db.Column(db.Boolean, default=False, nullable=False)
    events = db.relationship('Event', cascade="all,delete", backref='organizer', lazy=True)

    # roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.username}', '{self.email}', '{self.image_file}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(20), default='banner.jpg', nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.start_time}', '{self.end_time}', '{self.details}', '{self.banner}')"


class Participant(db.Model):
    __tablename__ = "participants"
    id = db.Column('particpant_id', db.Integer, primary_key=True)
    event = db.Column('event_id', db.Integer, nullable=False)
    first_name = db.Column('fname', db.String())
    last_name = db.Column('lname', db.String())
    email = db.Column('email', db.String())
    rfID = db.Column('contact', db.String())

    def __repr__(self):
        return f"User('{self.event}', '{self.first_name}', '{self.last_name}', '{self.email}', '{self.rfID}')"
