from datetime import datetime
from tapit import db, login_manager, app
from flask_login import UserMixin
# from flask_user import UserManager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

 

class Venue(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'), nullable=False)
    venue_name=db.Column(db.String(50), nullable=False)
    details=db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer(), nullable=False)
    equipment = db.Column(db.String(), nullable=False)
    image_file = db.Column(db.String(), nullable=False, default='banner.jpg')
    gallery = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    participants_list = db.Column(db.String(), nullable=False)
    is_archived = db.Column(db.String(), nullable=False)
    
    def __repr__(self):
        return f"User('{self.venue_name}', '{self.college_id}', '{self.capacity}', '{self.equipment}')"

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '{} - {}'.format(COLLEGEID.get(self.college), self.name)


class College(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =db.Column(db.String(50), nullable=False)
    abb = db.Column(db.String(50), nullable=False)
    img =db.Column(db.String(50), nullable=False)

    def __init__(self, name, abb, img):
        self.name = name
        self.abb = abb
        self.img = img

def init_colleges():
    is_existing = College.query.filter_by(id=1).first()
    if is_existing == None:
        newcollege = College(name='MSU-IIT', abb='MSU-IIT', img='IIT.jpg')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='MSU-IIT'
        is_existing.abb='MSU-IIT'
        is_existing.img='IIT.jpg'
        db.session.commit()

    is_existing = College.query.filter_by(id=2).first()
    if is_existing == None:
        newcollege = College(name='College of Engineering and Technology', abb='COET', img='COET.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Engineering and Technology'
        is_existing.abb='COET'
        is_existing.img='COET.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=3).first()
    if is_existing == None:
        newcollege = College(name='College of Science and Mathematics', abb='CSM', img='CSM.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Science and Mathematics'
        is_existing.abb='CSM'
        is_existing.img='CSM.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=4).first()
    if is_existing == None:
        newcollege = College(name='College of Education', abb='CED', img='CED.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Education'
        is_existing.abb='CED'
        is_existing.img='CED.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=5).first()
    if is_existing == None:
        newcollege = College(name='College of Arts and Social Science', abb='CASS', img='CASS.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Arts and Social Science'
        is_existing.abb='CASS'
        is_existing.img='CASS.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=6).first()
    if is_existing == None:
        newcollege = College(name='College of Business Administration and Accountancy', abb='CBAA', img='CBAA.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Business Administration and Accountancy'
        is_existing.abb='CBAA'
        is_existing.img='CBAA.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=7).first()
    if is_existing == None:
        newcollege = College(name='College of Nursing', abb='CON', img='nursing.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='College of Nursing'
        is_existing.abb='CON'
        is_existing.img='nursing.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=8).first()
    if is_existing == None:
        newcollege = College(name='College of Computer Studies', abb='CCS', img='SCS.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='School of Computer Studies'
        is_existing.abb='SCS'
        is_existing.img='SCS.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=9).first()
    if is_existing == None:
        newcollege = College(name='Integrated Developmental School', abb='IDS', img='IDS.png')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='Integrated Developmental School'
        is_existing.abb='IDS'
        is_existing.img='IDS.png'
        db.session.commit()

    is_existing = College.query.filter_by(id=10).first()
    if is_existing == None:
        newcollege = College(name='PRISM', abb='PRISM', img='PRISM.jpg')
        db.session.add(newcollege)
        db.session.commit()
    else:
        is_existing.name='PRISM'
        is_existing.abb='PRISM'
        is_existing.img='PRISM.jpg'
        db.session.commit()