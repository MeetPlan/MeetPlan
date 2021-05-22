from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, send_file, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from .models import *
from time import time
from random import random, choice
from . import db
from .main import getStrings, getLang
import os
import csv
from zipfile import ZipFile

import time

db = Blueprint('db', __name__)

def dbexport(continue2):
    users = User.query.all()
    with open('users.csv', mode='w+') as user_file:
        try:
            fieldnames = list(users[0].__dict__.keys())
            fieldnames.remove("_sa_instance_state")
            writer = csv.DictWriter(user_file, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                diction = user.__dict__
                del diction["_sa_instance_state"]
                writer.writerow(diction)
        except:
            if not continue2:
                return "Failed to export USERS"
    
    classes = Classes.query.all()
    with open('classes.csv', mode='w+') as classes_file:
        try:
            fieldnames = list(classes[0].__dict__.keys())
            fieldnames.remove("_sa_instance_state")
            writer = csv.DictWriter(classes_file, fieldnames=fieldnames)
            writer.writeheader()
            for clas in classes:
                diction = clas.__dict__
                del diction["_sa_instance_state"]
                writer.writerow(diction)
        except:
            if not continue2:
                return "Failed to export CLASSES"
    
    groups = MeetingGroup.query.all()
    with open('groups.csv', mode='w+') as groups_file:
        try:
            fieldnames = list(groups[0].__dict__.keys())
            fieldnames.remove("_sa_instance_state")
            writer = csv.DictWriter(groups_file, fieldnames=fieldnames)
            writer.writeheader()
            for clas in groups:
                diction = clas.__dict__
                del diction["_sa_instance_state"]
                writer.writerow(diction)
        except:
            if not continue2:
                return "Failed to export MEETING GROUPS"
    
    meetings = Meetings.query.all()
    with open('meetings.csv', mode='w+') as meetings_file:
        try:
            fieldnames = list(meetings[0].__dict__.keys())
            fieldnames.remove("_sa_instance_state")
            writer = csv.DictWriter(meetings_file, fieldnames=fieldnames)
            writer.writeheader()
            for clas in meetings:
                diction = clas.__dict__
                del diction["_sa_instance_state"]
                writer.writerow(diction)
        except:
            if not continue2:
                return "Failed to export MEETINGS"
    
    values = Values.query.all()
    with open('values.csv', mode='w+') as values_file:
        try:
            fieldnames = list(values[0].__dict__.keys())
            fieldnames.remove("_sa_instance_state")
            writer = csv.DictWriter(values_file, fieldnames=fieldnames)
            writer.writeheader()
            for clas in values:
                diction = clas.__dict__
                del diction["_sa_instance_state"]
                writer.writerow(diction)
        except:
            if not continue2:
                return "Failed to export VALUES"

@db.route("/db/export", methods=["GET"])
@login_required
def export():
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template("dbexport_load.html", strings=strings, name=current_user.first_name, role=current_user.role)

@db.route("/db/export", methods=["POST"])
@login_required
def exportPost():
    if request.args.get("continue") == "true":
        export = dbexport(True)
    else:
        export = dbexport(False)
    if export:
        flash(export)
    else:
        flash("Success :-)")
    return(redirect(url_for("db.export")))
