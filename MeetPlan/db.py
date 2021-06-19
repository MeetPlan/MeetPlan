import os
import csv
import time
import aiofiles

from fastapi import APIRouter, Request, Depends
from time import time
from random import random, choice

from . import db
from .constants import *
from .functiondeclarations import *
from .models import *
from .main import getStrings, getLang

db = APIRouter(
    tags=["db"]
)

async def dbexport(continue2):
    users = session.query(User).all()
    async with aiofiles.open('users.csv', mode='w+') as user_file:
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
    
    classes = session.query(Classes).all()
    async with aiofiles.open('classes.csv', mode='w+') as classes_file:
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
    
    groups = session.query(MeetingGroup).all()
    async with aiofiles.open('groups.csv', mode='w+') as groups_file:
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
    
    meetings = session.query(Meetings).all()
    async with aiofiles.open('meetings.csv', mode='w+') as meetings_file:
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
    
    values = session.query(Values).all()
    async with aiofiles.open('values.csv', mode='w+') as values_file:
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
    
    async with aiofiles.open("dbversion.txt", mode="w+") as dbversion:
        dbversion.write(MEETPLAN_DB_VERSION)
        dbversion.close()

@db.get("/db/export")
@login_required
def export(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template("dbexport_load.html", request=request, strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@db.post("/db/export")
@login_required
def exportPost(request: Request, continue2: str = None, current_user = Depends(manager)):
    if continue2 == "true":
        export = dbexport(True)
    else:
        export = dbexport(False)
    if export:
        flash(export)
    else:
        flash("Success :-)")
    return(redirect(request.url_for("export")))
