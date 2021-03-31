# models.py

from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    pmi = db.Column(db.String(100))
    role = db.Column(db.String(100))
    active = db.Column(db.Boolean)
    confirmed = db.Column(db.Boolean)
    meetings = db.relationship('Meetings', backref='user', lazy=True)

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    meetings_classes = db.relationship('Meetings', backref='classes', lazy=True)

class MeetingGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meetingGroup = db.Column(db.String(100))
    meetings = db.relationship('Meetings', backref='meetinggroup', lazy=True)

class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    hour = db.Column(db.Integer)
    required = db.Column(db.Boolean)
    grading = db.Column(db.Boolean)
    verifying = db.Column(db.Boolean)
    description = db.Column(db.Text())
    meetingApp = db.Column(db.String(100))
    link = db.Column(db.String(1000))
    teacher_id = db.Column(db.Integer)
    name = db.Column(db.String(100))
    meetingGroup = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey(Classes.id))
    teacher_id = db.Column(db.Integer, db.ForeignKey(User.id))
    group_id = db.Column(db.Integer, db.ForeignKey(MeetingGroup.id))

class Values(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    value = db.Column(db.String(1000))
