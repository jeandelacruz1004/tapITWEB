from datetime import datetime
from tapit import db, login_manager, app
from flask_login import UserMixin
# from flask_user import UserManager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    rfID = db.Column(db.String(50), unique=True, nullable=True)
    first_name = db.Column(db.String(25), unique=True, nullable=False)
    last_name = db.Column(db.String(25), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    contact = db.Column(db.String(20), unique=False, nullable=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), default='default.png', nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_student = db.Column(db.Boolean, default=True, nullable=False)
    is_faculty = db.Column(db.Boolean, default=False, nullable=False)
    events = db.relationship('Event', backref='organizer', lazy=True)

    # roles = db.relationship('Role', secondary='user_roles')

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.username}', '{self.email}', '{self.image_file}')"
#
#
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#
#
# class UserRoles():
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text, nullable=False)
    banner = db.Column(db.String(20), default='banner.jpg', nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"User('{self.title}', '{self.start_time}', '{self.end_time}', '{self.details}', '{self.banner}')"


class attendance(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    idnumber = db.Column(db.String(25), unique=True, nullable=False)
    firstname = db.Column(db.String(25), unique=True, nullable=False)
    lastname = db.Column(db.String(25), unique=True, nullable=False)
    gender = db.Column(db.String(25), unique=True, nullable=False)
    yearlevel = db.Column(db.String(20), unique=True, nullable=False)
    course_id = db.Column(db.String(20), unique=True, nullable=False)
    

    def __repr__(self):
        return f"User('{self.idnumber}', '{self.firstname}', '{self.lastname}', '{self.gender}', '{self.yearlevel}', '{self.course_id}')"
# user_manager = UserManager(app, db, User)
# db.create_all()

#
# if not User.query.filter(User.email == 'member@tapit.com').first():
#     user = User(
#         rfID='1234567899',
#         first_name='User',
#         last_name='Member',
#         username='testy',
#         email='member@tapit.com',
#         password=user_manager.hash_password('2212212')
#     )
#     db.session.add(user)
#     db.session.commit()
#
# if not User.query.filter(User.email == 'admin@tapit.com').first():
#     user = User(
#         rfID='1234567890',
#         first_name='Admin',
#         last_name='TapIt',
#         username='Admin',
#         email='admin@tapit.com',
#         password=user_manager.hash_password('regards')
#     )
#     user.roles.append(Role(name='Admin'))
#     user.roles.append(Role(name='Student'))
#     db.session.add(user)
#     db.session.commit()
#
