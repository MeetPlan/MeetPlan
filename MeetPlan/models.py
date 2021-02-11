# models.py

from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    active = db.Column(db.Boolean)
    meetings = db.relationship('Meetings', backref='user', lazy=True)

class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    hour = db.Column(db.Integer)
    required = db.Column(db.Boolean)
    grading = db.Column(db.Boolean)
    name = db.Column(db.String(100))
    className = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)