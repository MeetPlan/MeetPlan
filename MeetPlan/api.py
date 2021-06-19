from .models import *
from .tableutil import *
from werkzeug.security import check_password_hash
import os

from fastapi import APIRouter

api = APIRouter()

"""
    username = request.values.get('username')
    password = request.values.get('password')

    if not password or not username:
        return "400", 400
    else:
        if (loginUser(username, password)["success"] == True):
        else:
            return "403", 403
"""

def loginUser(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User.query.filter_by(username=email).first()
        if not user:
            json = {
                "success": False,
                "description": "No user with this username or email",
            }
            return json
    
    if not check_password_hash(user.password, password):
        json = {
            "success": False,
            "description": "Wrong password",
        }
        return json
    
    json = {
        "success": True,
        "description": "Successfully logged in",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "verified": user.confirmed
        }
    }
    return json

@api.route("/api/translations")
def getTranslations(request: Request):
    value = Values.query.filter_by(name="lang").first()
    if value:
        val = value.value
    else:
        val = Values(name="lang", value="en-US")
        db.session.add(val)
        db.session.commit()
        val = val.value
    
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'langs', val.lower()+'.json')
    strings = json.loads(open(json_url, encoding="utf-8").read(), encoding="utf-8")

    return jsonify(strings)

@api.route("/api/timetable", methods = ['GET'])
def getTable(request: Request):
    classname = request.values.get('class')

    username = request.values.get('username')
    password = request.values.get('password')

    if not classname:
        return "400", 400
    else:
        if (loginUser(username, password)["success"] == True):
            current_date = getDate()
            weeks = getWeekList(current_date)
            urnik = getOrderedListAPI(classname)
            return jsonify(urnik), 200
        else:
            return "403", 403

@api.route("/api/user")
def getUserInfo(request: Request):
    username = request.values.get('username')
    password = request.values.get('password')

    if not password or not username:
        return "400", 400
    else:
        user = loginUser(username, password)
        if user["success"] == True:
            return jsonify(user), 200
        else:
            return jsonify(user), 403

@api.route("/api/classes")
def getAllClasses(request: Request):
    username = request.values.get('username')
    password = request.values.get('password')

    if not password or not username:
        return "400", 400
    else:
        if (loginUser(username, password)["success"] == True):
            json = []
            for class1 in Classes.query.all():
                json.append({"name": class1.name})
            return jsonify({"classes": json}), 200
        else:
            return "403", 403

@api.route("/api/meeting/{int:id}")
def getMeeting(id):
    username = request.values.get('username')
    password = request.values.get('password')

    if not password or not username or not id:
        return "400", 400
    else:
        if (loginUser(username, password)["success"] == True):
            meeting = Meetings.query.filter_by(id=id).first()
            classes = Classes.query.filter_by(id=meeting.class_id).first()
            if meeting:
                json = {
                    "name": meeting.name,
                    "description": meeting.description,
                    "class": meeting.class_id,
                    "class": classes.name,
                    "grading": meeting.grading,
                    "verifying": meeting.verifying,
                    "required": meeting.required,
                    "meetingApp": meeting.meetingApp,
                    "link": meeting.link,
                    "date": meeting.date,
                    "hour": meeting.hour,
                    "id": meeting.id,
                    "teacher_id": meeting.teacher_id,
                    "group": meeting.meetingGroup
                }

                return jsonify(json), 200
            else:
                return "404 - Not found in database", 404
        else:
            return "403", 403