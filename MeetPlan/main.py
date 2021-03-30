from flask import *
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from .models import *
from .utils import *
from .tableutil import *
from .emptyobject import generateEmptyList
import json
import os

main = Blueprint('main', __name__)


def getStrings(lang):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'langs', lang+'.json')
    return json.loads(open(json_url, encoding="utf-8").read(), encoding="utf-8")

def getLang():
    value = Values.query.filter_by(name="lang").first()
    if value:
        return value.value
    else:
        val = Values(name="lang", value="en-US")
        db.session.add(val)
        db.session.commit()
        return val.value

"""
@main.route("/oobe", methods = ['POST', 'GET'])
def oobe():
    #if (request.method == 'POST'):
        #try:
    return render_template("oobe.html")
"""

@main.route("/", methods = ['GET', 'POST'])
@login_required
def dashboard():
    classname = request.values.get('class')

    lang = getLang().lower()
    strings = getStrings(lang)

    #print(classname)
    current_date = getDate()
    weeks = getWeekList(current_date)
    if (current_user.role == "admin" or current_user.role == "teacher"):
        isTeacher = "true"
    else:
        isTeacher = "false"
    if classname:
        urnik = getOrderedList(classname)
        return render_template("dashboard.html", name=current_user.first_name, classes=Classes.query.all(), role=current_user.role,
            mon=urnik["mon"],
            tue=urnik["tue"],
            wed=urnik["wed"],
            thu=urnik["thu"],
            fri=urnik["fri"],
            sat=urnik["sat"],
            dates = weeks,
            isTeacher = isTeacher,
            strings = strings
        )
    else:
        flash(strings["SELECT_CLASS"])

        return render_template("dashboard.html",
            name=current_user.first_name,
            classes=Classes.query.all(),
            mon=generateEmptyList(), 
            tue=generateEmptyList(),
            wed=generateEmptyList(),
            thu=generateEmptyList(),
            fri=generateEmptyList(),
            sat=generateEmptyList(),
            role=current_user.role,
            dates=weeks,
            isTeacher=isTeacher,
            strings=strings
        )

@main.route("/class/add", methods=["GET"])
@login_required
def addClass():
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template("addclass.html", classes = Classes.query.all(), role=current_user.role, name=current_user.first_name, strings=strings)

@main.route("/class/add", methods=["POST"])
@login_required
def addClassPost():
    name = request.form["class"]
    print(name)
    newClass = Classes(name=name)
    db.session.add(newClass)
    db.session.commit()
    return redirect(url_for("main.addClass"))

@login_required
@main.route("/meeting/picker", methods=["GET"])
def meetingPicker():
    lang = getLang().lower()
    strings = getStrings(lang)

    if (current_user.role == "admin" or current_user.role == "teacher"):
        isTeacher = "true"
    else:
        isTeacher = "false"
    current_date = getDate()
    weeks = getWeekList(current_date)
    return render_template("meetingpicker.html",
        mon=[], tue=[], wed=[], thu=[], fri=[], sat=[],
        role=current_user.role, name=current_user.first_name,
        classes = Classes.query.all(),
        isTeacher = isTeacher,
        dates = weeks,
        strings = strings
    )

@main.route("/meeting/add", methods=["GET"])
@login_required
def meetingAdd():
    lang = getLang().lower()
    strings = getStrings(lang)

    if current_user.role == "admin" or current_user.role == "teacher":
        return render_template("addmeeting.html",
            mon=[], tue=[], wed=[], thu=[], fri=[], sat=[],
            role=current_user.role,
            name=current_user.first_name,
            classes = Classes.query.all(),
            strings = strings
        ), 200
    else:
        abort(403)

@main.route("/meeting/edit/<int:id>", methods=["GET"])
@login_required
def meetingEdit(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = Meetings.query.filter_by(id=id).first()
    print(meeting.meetingApp)
    if meeting:
        if current_user.role == "admin" or current_user.id == meeting.teacher_id:
            return render_template("addmeeting.html",
                mon=[], tue=[], wed=[], thu=[], fri=[], sat=[],
                role=current_user.role,
                name=current_user.first_name,
                classes = Classes.query.all(),
                meetingName = meeting.name,
                date = meeting.date,
                className = meeting.className,
                meetingHour = str(meeting.hour),
                strings = strings
            ), 200
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/approve/<int:id>", methods=["GET"])
@login_required
def approveUser(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = User.query.filter_by(id=id).first()
    if user:
        if (current_user.role == "admin"):
            user.confirmed = True
            db.session.commit()
            return redirect(url_for("main.allUsers"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/promote/<role>/<int:id>", methods=["GET"])
@login_required
def promoteUser(role, id):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = User.query.filter_by(id=id).first()
    if user:
        if (current_user.role == "admin"):
            if (role == "teacher"):
                user.role = "teacher"
            elif (role == "administrator"):
                user.role = "admin"
            else:
                flash(strings["UNKNOWN_ROLE"])
                return redirect(url_for("main.allUsers"))
            db.session.commit()
            return redirect(url_for("main.allUsers"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/demote/<int:id>", methods=["GET"])
@login_required
def demoteUser(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = User.query.filter_by(id=id).first()
    if user:
        if (current_user.role == "admin"):
            user.role = "student"
            db.session.commit()
            return redirect(url_for("main.allUsers"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/decline/<int:id>", methods=["GET"])
@login_required
def declineUser(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = User.query.filter_by(id=id).first()
    if user:
        if (current_user.role == "admin"):
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for("main.allUsers"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/delete/meeting/<int:id>", methods=["GET"])
@login_required
def deleteMeeting(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = Meetings.query.filter_by(id=id).first()
    print(meeting.teacher_id)
    if meeting:
        if (current_user.role == "admin" or current_user.id == meeting.teacher_id):
            db.session.delete(meeting)
            db.session.commit()
            return redirect(url_for("main.allMeetings"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/meeting/view/<int:id>", methods=["GET"])
@login_required
def meetingView(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = Meetings.query.filter_by(id=id).first()
    if meeting:
        weeklist = getWeekList(getDate())
        #print(weeklist)
        #print(meeting.date)
        if (meeting.date in weeklist or current_user.role == "teacher" or current_user.role == "admin"):
            return render_template("meetingview.html", meeting=meeting, strings=strings, name=current_user.first_name, role=current_user.role)
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)

@main.route("/meeting/add", methods=["POST"])
@login_required
def meetingAddPost():
    if (current_user.role == "teacher" or current_user.role == "admin"):
        name = request.form.get('name')
        desc = request.form.get('desc')
        grading = request.form.get('grading')
        mandatory = request.form.get('mandatory')
        checking = request.form.get('checking')
        app = request.form.get('confapp')
        classname = request.form.get('class')
        date = request.form.get('date')
        hour = request.form.get('hour')
        link = request.form.get('urlID')
        print(classname)
        print(date)

        ifmeeting = Meetings.query.filter_by(date=date, hour=hour, className=classname).first()
        lang = getLang().lower()
        strings = getStrings(lang)

        if ifmeeting:
            flash(strings["ALREADY_RESERVED"])
            return redirect(url_for("main.meetingAdd"))

        if (app == "zoom"):
            link = "https://zoom.us/j/"+link
        elif (app == "gmeet"):
            link = "https://meet.google.com/"+link
        else:
            link = link

        if (not grading):
            grading = False
        else:
            grading = True
        
        if (not mandatory):
            mandatory = False
        else:
            mandatory = True
        
        if (not checking):
            checking = False
        else:
            checking = True
        
        classID = Classes.query.filter_by(name=classname).first()

        if (not classID):
            return "<h1>500 Internal Server Error</h1><br>No class with this name", 500
        
        print(classID.name)

        new_meeting = Meetings(
            class_id=classID.id, required=mandatory, grading=grading, verifying=checking,
            description=desc, meetingApp=app, name=name, className=classID.name, link=link,
            date=date, hour=hour, teacher_id=current_user.id
        )

        db.session.add(new_meeting)
        db.session.commit()

        return redirect(url_for("main.meetingAdd"))
    else:
        abort(403)

@main.route("/meeting/edit/<int:id>", methods=["POST"])
@login_required
def meetingEditPost(id):
    meeting = Meetings.query.filter_by(id=id).first()
    if meeting:
        if (current_user.role == "teacher" or current_user.role == "admin"):
            name = request.form.get('name')
            desc = request.form.get('desc')
            grading = request.form.get('grading')
            mandatory = request.form.get('mandatory')
            checking = request.form.get('checking')
            app = request.form.get('confapp')
            classname = request.form.get('class')
            date = request.form.get('date')
            hour = request.form.get('hour')
            link = request.form.get('urlID')
            print(classname)
            print(date)

            ifmeeting = Meetings.query.filter_by(date=date, hour=hour, className=classname).first()
            lang = getLang().lower()
            strings = getStrings(lang)

            if ifmeeting:
                flash(strings["ALREADY_RESERVED"])
                return redirect(url_for("main.meetingAdd"))

            if (app == "zoom"):
                link = "https://zoom.us/j/"+link
            elif (app == "gmeet"):
                link = "https://meet.google.com/"+link
            else:
                link = link

            if (not grading):
                grading = False
            else:
                grading = True
            
            if (not mandatory):
                mandatory = False
            else:
                mandatory = True
            
            if (not checking):
                checking = False
            else:
                checking = True
            
            classID = Classes.query.filter_by(name=classname).first()

            if (not classID):
                return "<h1>500 Internal Server Error</h1><br>No class with this name", 500
            
            print(classID.name)

            meeting.class_id=classID.id
            meeting.required=mandatory
            meeting.grading=grading
            meeting.verifying=checking
            meeting.description=desc
            meeting.meetingApp=app
            meeting.name=name
            meeting.className=classID.name
            meeting.link=link
            meeting.date=date
            meeting.hour=hour
            meeting.teacher_id=current_user.id

            db.session.commit()

            return redirect(url_for("main.meetingAdd"))
        else:
            abort(403)

@main.route("/admin/users")
@login_required
def allUsers():
    lang = getLang().lower()
    strings = getStrings(lang)

    if (current_user.role == "admin"):
        pending = User.query.filter_by(confirmed=False).all()
        users = User.query.filter_by(confirmed=True).all()
        return render_template("allusers.html", users=users, pendingusers=pending, strings=strings, name=current_user.first_name, role=current_user.role)
    else:
        abort(403)

@main.route("/admin/meetings")
@login_required
def allMeetings():
    lang = getLang().lower()
    strings = getStrings(lang)

    if (current_user.role == "admin"):
        meetings = Meetings.query.all()
        return render_template("allmeetings.html", meetings=meetings, strings=strings, name=current_user.first_name, role=current_user.role)
    elif (current_user.role == "teacher"):
        meetings = Meetings.query.filter_by(teacher_id=current_user.id).all()
        return render_template("allmeetings.html", meetings=meetings, strings=strings, name=current_user.first_name, role=current_user.role)
    else:
        abort(403)

@main.route("/settings", methods=["GET"])
@login_required
def settings():
    lang = getLang().lower()
    strings = getStrings(lang)

    if (current_user.role == "admin"):
        return render_template("settings.html", strings=strings, name=current_user.first_name, role=current_user.role)
    else:
        abort(403)

@main.route("/settings", methods=["POST"])
@login_required
def settingsPost():
    if (current_user.role == "admin"):
        lang = request.form.get('lang')
        val = Values.query.filter_by(name="lang").first()
        val.value = lang
        db.session.commit()
        return redirect(url_for("main.settings"))
    else:
        abort(403)

@main.app_errorhandler(403)
def error403(e):
    lang = getLang().lower()
    strings = getStrings(lang)

    try:
        name = current_user.first_name
    except:
        name = ""

    return render_template("403.html", strings=strings, name=name)