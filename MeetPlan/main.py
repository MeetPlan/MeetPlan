from flask import *
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from .models import *
from .utils import *
from .tableutil import *
from .emptyobject import generateEmptyList
import json
import os
import sys

main = Blueprint('main', __name__)


def getStrings(lang):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'langs', lang + '.json')
    if sys.version_info <= (3, 8):
        print("Running at 3.8 or lower")
        return json.loads(open(json_url, encoding="utf-8").read(), encoding="utf-8")
    else:
        return json.loads(open(json_url, encoding="utf-8").read())


def getLang():
    value = Values.query.filter_by(name="lang").first()
    if value:
        return value.value
    else:
        val = Values(name="lang", value="en-US")
        db.session.add(val)
        db.session.commit()
        return val.value


def getMax():
    value = Values.query.filter_by(name="max").first()
    if value:
        return value.value
    else:
        val = Values(name="max", value="3")
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


@main.route("/", methods=['GET', 'POST'])
@login_required
def dashboard():
    classname = request.values.get('class')

    lang = getLang().lower()
    strings = getStrings(lang)

    # print(classname)
    current_date = getDate()
    weeks = getWeekList(current_date)
    isWeekend = False
    weekend = weeks[5:]
    nextweekday = current_date + timedelta(days=7)
    nextweek = getWeekList(nextweekday)
    date = str(current_date).split(" ")[0]
    if date in weekend or current_user.role == "teacher" or current_user.role == "admin":
        isWeekend = True
    if (current_user.role == "admin" or current_user.role == "teacher"):
        isTeacher = "true"
    else:
        isTeacher = "false"
    if classname:
        urnik = getOrderedList(classname)
        urniknext = getOrderedList(classname, week=nextweek)
        return render_template("dashboard.html", name=current_user.first_name, classes=Classes.query.all(),
                               role=current_user.role,
                               mon=urnik["mon"],
                               tue=urnik["tue"],
                               wed=urnik["wed"],
                               thu=urnik["thu"],
                               fri=urnik["fri"],
                               sat=urnik["sat"],
                               dates=weeks,
                               isTeacher=isTeacher,
                               strings=strings,
                               classname=classname,
                               isWeekend=isWeekend,
                               monnext=urniknext["mon"],
                               tuenext=urniknext["tue"],
                               wednext=urniknext["wed"],
                               thunext=urniknext["thu"],
                               frinext=urniknext["fri"],
                               satnext=urniknext["sat"],
                               nextdates=nextweek
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
                               strings=strings,
                               classname=None
                               )


@main.route("/print")
@login_required
def printTable():
    classname = request.values.get('class')
    bare = request.values.get('bare')

    current_date = getDate()
    weeks = getWeekList(current_date)

    lang = getLang().lower()
    strings = getStrings(lang)

    if classname:
        print(bare)
        if bare == "true":
            print("True")
            urnik = getOrderedList(classname)

            return render_template("bareprint.html",
                                   mon=urnik["mon"],
                                   tue=urnik["tue"],
                                   wed=urnik["wed"],
                                   thu=urnik["thu"],
                                   fri=urnik["fri"],
                                   sat=urnik["sat"],
                                   dates=weeks,
                                   strings=strings
                                   )
        else:
            urnik = getOrderedList(classname)

            return render_template("print.html",
                                   mon=urnik["mon"],
                                   tue=urnik["tue"],
                                   wed=urnik["wed"],
                                   thu=urnik["thu"],
                                   fri=urnik["fri"],
                                   sat=urnik["sat"],
                                   dates=weeks,
                                   strings=strings,
                                   classname=classname,
                                   week=weeks[0] + strings["TO"] + weeks[-1]
                                   )
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)


@main.route("/class/add", methods=["GET"])
@login_required
def addClass():
    if current_user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)

        return render_template("addclass.html", classes=Classes.query.all(), role=current_user.role,
                               name=current_user.first_name, strings=strings)
    else:
        abort(403)


@main.route("/class/add", methods=["POST"])
@login_required
def addClassPost():
    if current_user.role == "admin":
        name = request.form["class"]
        print(name)
        newClass = Classes(name=name)
        db.session.add(newClass)
        db.session.commit()
        return redirect(url_for("main.addClass"))
    else:
        abort(403)


@main.route("/group/add", methods=["GET"])
@login_required
def addGroup():
    if current_user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)

        return render_template("addmeetinggroups.html", groups=MeetingGroup.query.all(), role=current_user.role,
                               name=current_user.first_name, strings=strings)
    else:
        abort(403)


@main.route("/group/add", methods=["POST"])
@login_required
def addGroupPost():
    if current_user.role == "admin":
        name = request.form["group"]
        print(name)
        newClass = MeetingGroup(meetingGroup=name)
        db.session.add(newClass)
        db.session.commit()
        return redirect(url_for("main.addGroup"))
    else:
        abort(403)


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
                           classes=Classes.query.all(),
                           isTeacher=isTeacher,
                           dates=weeks,
                           strings=strings
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
                               classes=Classes.query.all(),
                               strings=strings,
                               groups=MeetingGroup.query.all()
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
    class1 = Classes.query.filter_by(id=meeting.class_id).first()
    if meeting:
        if current_user.role == "admin" or current_user.id == meeting.teacher_id:
            return render_template("addmeeting.html",
                                   mon=[], tue=[], wed=[], thu=[], fri=[], sat=[],
                                   role=current_user.role,
                                   name=current_user.first_name,
                                   classes=Classes.query.all(),
                                   meetingName=meeting.name,
                                   date=meeting.date,
                                   mandatory=meeting.required,
                                   grading=meeting.grading,
                                   verifying=meeting.verifying,
                                   className=class1.name,
                                   meetingHour=str(meeting.hour),
                                   strings=strings,
                                   groupsel=meeting.meetingGroup,
                                   groups=MeetingGroup.query.all()
                                   ), 200
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)


@main.route("/approve/<int:id>", methods=["GET"])
@login_required
def approveUser(id: int):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = User.query.filter_by(id=id).first()
    if user:
        if current_user.role == "admin":
            user.confirmed = True
            db.session.commit()
            return redirect(url_for("main.allUsers"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)


@main.route("/user/password/change", methods=["GET"])
@login_required
def changePassword():
    lang = getLang().lower()
    strings = getStrings(lang)

    block_pass = True
    if current_user.role == "student":
        v = Values.query.filter_by(name="block_pass_change_student").first()
        print(v.value)
        if v is None:
            v = Values(name="block_pass_change_student", value=None)
            db.session.add(v)
            db.session.commit()
        if v.value != "on":
            block_pass = False
    elif current_user.role == "teacher":
        v = Values.query.filter_by(name="block_pass_change_teacher").first()
        if v is None:
            v = Values(name="block_pass_change_teacher", value=None)
            db.session.add(v)
            db.session.commit()
        if v.value != "on":
            block_pass = False
    else:
        block_pass = False
    if not block_pass:
        return render_template("change_pass.html", strings=strings, name=current_user.first_name, role=current_user.role)
    else:
        flash(strings["YOU_CANNOT_CHANGE_PASSWORD"])
        return redirect(url_for("main.dashboard"))


@main.route("/user/password/change", methods=["POST"])
@login_required
def changePasswordPost():
    lang = getLang().lower()
    strings = getStrings(lang)

    block_pass = True
    if current_user.role == "student":
        v = Values.query.filter_by(name="block_pass_change_student").value
        if v != "on":
            block_pass = False
    elif current_user.role == "teacher":
        v = Values.query.filter_by(name="block_pass_change_teacher").value
        if v != "on":
            block_pass = False
    else:
        block_pass = False
    if not block_pass:
        oldpass = request.form.get("oldpass")
        newpass = request.form.get("newpass")
        newpassrepeat = request.form.get("newpassrepeat")
        if newpass != newpassrepeat:
            flash(strings["PASSWORDS_DONT_MATCH"])
            return redirect(url_for("main.changePassword"))
        if newpass == oldpass:
            flash(strings["PASSWORD_CANNOT_EQUAL_OLD"])
            return redirect(url_for("main.changePassword"))
        if not check_password_hash(current_user.password, oldpass):
            flash(strings["OLD_PASS_DOESNT_MATCH"])
            return redirect(url_for("main.changePassword"))
        user = User.query.filter_by(id=current_user.id).first()
        user.password = generate_password_hash(newpass, method='sha256')
        db.session.commit()
        flash(strings["PASSWORD_CHANGED"])
        return redirect(url_for("main.changePassword"))
    else:
        abort(403)

@main.route("/user/settings", methods=["GET"])
@login_required
def userSettings():
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template(
        "usersettings.html",
        enablePMI=current_user.role != "student",
        currentPMI=current_user.pmi,
        strings=strings,
        name=current_user.first_name,
        role=current_user.role
    )


@main.route("/user/settings", methods=["POST"])
@login_required
def userSettingsPost():
    pmi = request.form.get("pmi")
    if current_user.role != "student":
        user = User.query.filter_by(id=current_user.id).first()
        user.pmi = pmi
    db.session.commit()
    return redirect(url_for("main.userSettings"))


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


@main.route("/group/view/<int:id>", methods=["GET", "POST"])
@login_required
def groupView(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = Meetings.query.filter_by(id=id).first()
    classname = Classes.query.filter_by(id=meeting.class_id).first()
    print(classname)
    if meeting:
        weeklist = getWeekList(getDate())
        current_date = str(getDate()).split(" ")[0]
        isWeekend = False
        if current_date in weeklist[5:]:
            isWeekend = True
        if meeting.date in weeklist or isWeekend or current_user.role == "teacher" or current_user.role == "admin":
            if meeting.group_id:
                print("Meeting has a Group ID")
                meeting = Meetings.query.filter_by(date=meeting.date, group_id=meeting.group_id,
                                                   hour=meeting.hour).all()
                print(meeting[0].group_id)
                return render_template("groupview.html", meetings=meeting, strings=strings, role=current_user.role,
                                       name=current_user.first_name)
            else:
                return redirect(url_for("main.meetingView"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=current_user.first_name, role=current_user.role)


@main.route("/meeting/view/<int:id>", methods=["GET"])
@login_required
def meetingView(id):
    lang = getLang().lower()
    strings = getStrings(lang)

    continue2 = request.args.get("continue")

    meeting = Meetings.query.filter_by(id=id).first()
    classname = Classes.query.filter_by(id=meeting.class_id).first()
    print(classname)
    if meeting:
        weeklist = getWeekList(getDate())
        current_date = str(getDate()).split(" ")[0]
        isWeekend = False
        if current_date in weeklist[5:]:
            isWeekend = True
        if meeting.date in weeklist or isWeekend or current_user.role == "teacher" or current_user.role == "admin":
            print(continue2)
            if continue2 == "true":
                return render_template("meetingview.html", meeting=meeting, strings=strings,
                                       name=current_user.first_name, role=current_user.role, className=classname.name)
            if meeting.group_id:
                print("Meeting has a Group ID")
                meeting = Meetings.query.filter_by(date=meeting.date, group_id=meeting.group_id,
                                                   hour=meeting.hour).all()
                return redirect(url_for("main.groupView", id=id))
            else:
                return render_template("meetingview.html", meeting=meeting, strings=strings,
                                       name=current_user.first_name, role=current_user.role, className=classname.name)
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
        pmi = request.form.get('pmi')
        group = request.form.get('group')
        """
        print(classname)
        print(date)
        print(pmi)
        print(group)
        """

        lang = getLang().lower()
        strings = getStrings(lang)

        if pmi == "yes":
            if current_user.pmi:
                link = current_user.pmi
            else:
                flash(strings["NO_PMI_SET"])
                return redirect(url_for("main.meetingAdd"))

        classID = Classes.query.filter_by(name=classname).first()

        if group != "none":
            print("ok, grouped")
            group = MeetingGroup.query.filter_by(meetingGroup=group).first()
            groupid = group.id
            groupName = group.meetingGroup
        else:
            groupid = None
            groupName = None

        ifmeeting = Meetings.query.filter_by(date=date, hour=hour, class_id=classID.id).all()
        hmeeting = Meetings.query.filter_by(date=date, class_id=classID.id).all()
        print(hmeeting)

        maximum = int(getMax())
        print(maximum)

        groups = []
        index = 0

        for meeting in hmeeting:
            if meeting.group_id:
                if meeting.group_id not in groups:
                    groups.append(meeting.group_id)
                    index += 1
            else:
                index += 1
        print(index)

        if index >= maximum:
            flash(strings["MAXIMUM_EXCEEDED"])
            return redirect(url_for("main.meetingAdd"))
        
        if ifmeeting and ifmeeting[0].group_id != groupid:
            flash(strings["ALREADY_RESERVED"])
            return redirect(url_for("main.meetingAdd"))

        if (app == "zoom"):
            link = "https://zoom.us/j/" + link
        elif (app == "gmeet"):
            link = "https://meet.google.com/" + link
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

        if (not classID):
            return "<h1>500 Internal Server Error</h1><br>No class with this name", 500

        new_meeting = Meetings(
            class_id=classID.id,
            required=mandatory,
            grading=grading,
            verifying=checking,
            description=desc,
            meetingApp=app,
            name=name,
            link=link,
            date=date,
            hour=hour,
            teacher_id=current_user.id,
            meetingGroup=groupName,
            group_id=groupid
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
            pmi = request.form.get("pmi")
            group = request.form.get("group")
            print(group)
            print(date)

            groupName = MeetingGroup.query.filter_by(meetingGroup=group).first()
            meetinggroupname = None
            groupid = None
            if groupName:
                meetinggroupname = groupName.meetingGroup
                groupid = groupName.id

            className = Classes.query.filter_by(name=classname).first()

            ifmeeting = Meetings.query.filter_by(date=date, hour=hour, class_id=className.id).all()
            lang = getLang().lower()
            strings = getStrings(lang)

            ok = False
            print(ifmeeting)
            if len(ifmeeting) == 0:
                ok = True
            for i in ifmeeting:
                # Here is a problem
                # Other teacher in group could probably edit it.
                # I will fix this as soon as possible
                if i.teacher_id == current_user.id or current_user.admin:
                    ok = True
            if not ok:
                flash(strings["ALREADY_RESERVED"])
                return redirect(url_for("main.meetingAdd"))

            if pmi == "yes":
                link = current_user.pmi

            if not link:
                flash(strings["INVALID_LINK"])
                return redirect(url_for("main.meetingAdd"))

            if (app == "zoom"):
                link = "https://zoom.us/j/" + link
            elif (app == "gmeet"):
                link = "https://meet.google.com/" + link
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

            meeting.class_id = classID.id
            meeting.required = mandatory
            meeting.grading = grading
            meeting.verifying = checking
            meeting.description = desc
            meeting.meetingApp = app
            meeting.name = name
            meeting.className = classID.name
            meeting.link = link
            meeting.date = date
            meeting.hour = hour
            meeting.teacher_id = current_user.id
            meeting.meetingGroup = meetinggroupname
            meeting.group_id = groupid


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
        return render_template("allusers.html", users=users, pendingusers=pending, strings=strings,
                               name=current_user.first_name, role=current_user.role)
    else:
        abort(403)


@main.route("/admin/meetings")
@login_required
def allMeetings():
    lang = getLang().lower()
    strings = getStrings(lang)

    if (current_user.role == "admin"):
        meetings = Meetings.query.all()
        return render_template("allmeetings.html", meetings=meetings, strings=strings, name=current_user.first_name,
                               role=current_user.role)
    elif (current_user.role == "teacher"):
        meetings = Meetings.query.filter_by(teacher_id=current_user.id).all()
        return render_template("allmeetings.html", meetings=meetings, strings=strings, name=current_user.first_name,
                               role=current_user.role)
    else:
        abort(403)


@main.route("/settings", methods=["GET"])
@login_required
def settings():
    lang = getLang().lower()
    strings = getStrings(lang)

    if current_user.role == "admin":
        q = Values.query.filter_by(name="blockregistration").first().value

        bl_pass_change_student = Values.query.filter_by(name="block_pass_change_student").first()
        if bl_pass_change_student is None:
            new = Values(name="block_pass_change_student", value=None)
            db.session.add(new)
            db.session.commit()
            bl_pass_change_student = new.value
        else:
            bl_pass_change_student = bl_pass_change_student.value

        bl_pass_change_teacher = Values.query.filter_by(name="block_pass_change_teacher").first()
        if bl_pass_change_student is None:
            new = Values(name="block_pass_change_teacher", value=None)
            db.session.add(new)
            db.session.commit()
            bl_pass_change_teacher = new.value
        else:
            bl_pass_change_teacher = bl_pass_change_teacher.value

        return render_template("settings.html", strings=strings, name=current_user.first_name, role=current_user.role,
                               max=getMax(), blockregister=q, lang=lang,
                               block_pass_change_student=bl_pass_change_student,
                               block_pass_change_teacher=bl_pass_change_teacher
                               )
    else:
        abort(403)


@main.route("/settings", methods=["POST"])
@login_required
def settingsPost():
    if current_user.role == "admin":
        lang = request.form.get('lang')
        maxmeet = request.form.get('max')
        blockregister = request.form.get("blockregister")
        block_pass_change_student = request.form.get("block_pass_change_student")
        block_pass_change_teacher = request.form.get("block_pass_change_teacher")

        max3 = Values.query.filter_by(name="max").first()
        max3.value = str(maxmeet)

        val = Values.query.filter_by(name="lang").first()
        val.value = lang

        blockr = Values.query.filter_by(name="blockregistration").first()
        if blockregister is None:
            blockregister = "0"
        else:
            blockregister = "1"
        blockr.value = blockregister

        block_pass_change_student_db = Values.query.filter_by(name="block_pass_change_student").first()
        if block_pass_change_student_db is None:
            new = Values(name="block_pass_change_student", value=block_pass_change_student)
            db.session.add(new)
        else:
            block_pass_change_student_db.value = block_pass_change_student
        block_pass_change_teacher_db = Values.query.filter_by(name="block_pass_change_teacher").first()
        if block_pass_change_teacher_db is None:
            new = Values(name="block_pass_change_teacher", value=block_pass_change_teacher)
            db.session.add(new)
        else:
            block_pass_change_teacher_db.value = block_pass_change_teacher

        db.session.commit()
        return redirect(url_for("main.settings"))
    else:
        abort(403)


@main.route("/class/delete/<int:id>")
@login_required
def delete_class(id: int):
    if current_user.role == "admin":
        meetings = Meetings.query.filter_by(class_id=id).all()
        for meeting in meetings:
            db.session.delete(meeting)
        class1 = Classes.query.filter_by(id=id).first()
        db.session.delete(class1)
        db.session.commit()
        return redirect(url_for("main.addClass"))
    else:
        abort(403)


@main.route("/meetinggroup/delete/<int:id>")
@login_required
def delete_group(id: int):
    if current_user.role == "admin":
        meetings = Meetings.query.filter_by(group_id=id).all()
        for meeting in meetings:
            db.session.delete(meeting)
        group = MeetingGroup.query.filter_by(id=id).first()
        db.session.delete(group)
        db.session.commit()
        return redirect(url_for("main.addGroup"))
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
