from fastapi import APIRouter, Request, status, Form, Depends
from typing import Optional
from starlette.responses import RedirectResponse
from .utils import *
from .tableutil import *
from .models import *
from .emptyobject import generateEmptyList
import json
import os
import sys

from .functiondeclarations import *
from .constants import templatemanager, render_template, redirect, manager, flash

main = APIRouter(
    tags=["main"]
)

def getStrings(lang):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'langs', lang+'.json')
    if sys.version_info <= (3, 8):
        print("Running at 3.8 or lower")
        return json.loads(open(json_url, encoding="utf-8").read(), encoding="utf-8")
    else:
        return json.loads(open(json_url, encoding="utf-8").read())

def getLang():
    value = session.query(Values).filter_by(name="lang").first()
    #value = Values.query.filter_by(name="lang").first()
    if value:
        return value.value
    else:
        val = Values(name="lang", value="en-US")
        session.add(val)
        session.commit()
        return val.value

def getMax():
    value = session.query(Values).filter_by(name="max").first()
    if value:
        return value.value
    else:
        val = Values(name="max", value="3")
        session.add(val)
        session.commit()
        return val.value

"""
@main.route("/oobe", methods = ['POST', 'GET'])
def oobe(request: Request):
    #if (request.method == 'POST'):
        #try:
    return render_template("oobe.html")
"""

@main.get("/")
@login_required
def dashboard(request: Request, classname: Optional[str] = None, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    print(classname)
    current_date = getDate()
    weeks = getWeekList(current_date)
    if (request.state.user.role == "admin" or request.state.user.role == "teacher"):
        isTeacher = "true"
    else:
        isTeacher = "false"
    if classname:
        urnik = getOrderedList(classname)
        return templatemanager.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "name": request.state.user.first_name,
                "classes": session.query(Classes).all(),
                "role": request.state.user.role,
                "mon": urnik["mon"],
                "tue": urnik["tue"],
                "wed": urnik["wed"],
                "thu": urnik["thu"],
                "fri": urnik["fri"],
                "sat": urnik["sat"],
                "dates": weeks,
                "isTeacher": isTeacher,
                "strings": strings,
                "classname": classname
            }
        )
    else:
        #flash(strings["SELECT_CLASS"])

        return templatemanager.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "name": request.state.user.first_name,
                "classes": session.query(Classes).all(),
                "mon": generateEmptyList(), 
                "tue": generateEmptyList(),
                "wed": generateEmptyList(),
                "thu": generateEmptyList(),
                "fri": generateEmptyList(),
                "sat": generateEmptyList(),
                "role": request.state.user.role,
                "dates": weeks,
                "isTeacher": isTeacher,
                "strings": strings,
                "classname": None
            }
        )

@main.get("/print")
@login_required
def printTable(request: Request, classname: str, bare: str = "false", current_user = Depends(manager)):
    current_date = getDate()
    weeks = getWeekList(current_date)

    lang = getLang().lower()
    strings = getStrings(lang)

    if classname:
        print(bare)
        if bare == "true":
            print("True")
            urnik = getOrderedList(classname)
        
            return render_template(
                    "bareprint.html",
                    request=request,
                    mon=urnik["mon"],
                    tue=urnik["tue"],
                    wed=urnik["wed"],
                    thu=urnik["thu"],
                    fri=urnik["fri"],
                    sat=urnik["sat"],
                    dates = weeks,
                    strings = strings
                )
        else:
            urnik = getOrderedList(classname)
        
            return render_template(
                    "print.html",
                    request=request,
                    mon=urnik["mon"],
                    tue=urnik["tue"],
                    wed=urnik["wed"],
                    thu=urnik["thu"],
                    fri=urnik["fri"],
                    sat=urnik["sat"],
                    dates = weeks,
                    strings = strings,
                    classname=classname,
                    week=weeks[0]+strings["TO"]+weeks[-1]
                )
    else:
        return render_template("404db.html", request=request, strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@main.get("/class/add")
@login_required
def addClass(request: Request, current_user = Depends(manager)):
    if request.state.user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)

        return templatemanager.TemplateResponse(
            "addclass.html",
            {
                "request": request,
                "classes": session.query(Classes).all(),
                "role": request.state.user.role,
                "name": request.state.user.first_name,
                "strings": strings
            }
        )
    else:
        abort(403)

@main.post("/class/add")
@login_required
def addClassPost(request: Request, name: str = Form(...), current_user = Depends(manager)):
    if request.state.user.role == "admin":
        print(name)
        newClass = Classes(name=name)
        session.add(newClass)
        session.commit()
        return RedirectResponse(request.url_for("addClass"), status_code=status.HTTP_303_SEE_OTHER)
    else:
        abort(403)

@main.get("/group/add")
@login_required
def addGroup(request: Request, current_user = Depends(manager)):
    if request.state.user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)

        return templatemanager.TemplateResponse(
            "addmeetinggroups.html",
            {
                "request": request,
                "groups": session.query(MeetingGroup).all(),
                "role": request.state.user.role,
                "name": request.state.user.first_name,
                "strings": strings
            }
        )
    else:
        abort(403)

@main.post("/group/add")
@login_required
def addGroupPost(request: Request, group: str = Form(...), current_user = Depends(manager)):
    if request.state.user.role == "admin":
        name = group
        print(name)
        newClass = MeetingGroup(meetingGroup=name)
        session.add(newClass)
        session.commit()
        return RedirectResponse(request.url_for("addGroup"), status_code=status.HTTP_303_SEE_OTHER)
    else:
        abort(403)

@login_required
@main.get("/meeting/picker")
def meetingPicker(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    if (request.state.user.role == "admin" or request.state.user.role == "teacher"):
        isTeacher = "true"
    else:
        isTeacher = "false"
    current_date = getDate()
    weeks = getWeekList(current_date)
    return render_template("meetingpicker.html",
        mon=[], tue=[], wed=[], thu=[], fri=[], sat=[],
        role=request.state.user.role, name=request.state.user.first_name,
        classes = Classes.query.all(),
        isTeacher = isTeacher,
        dates = weeks,
        strings = strings
    )

@main.get("/meeting/add")
@login_required
def meetingAdd(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    if request.state.user.role == "admin" or request.state.user.role == "teacher":
        return templatemanager.TemplateResponse("addmeeting.html",
            {
                "request": request,
                "mon": [], "tue": [], "wed": [], "thu": [], "fri": [], "sat": [],
                "role": request.state.user.role,
                "name": request.state.user.first_name,
                "classes": session.query(Classes).all(),
                "strings": strings,
                "groups": session.query(MeetingGroup).all()
            }
        )
    else:
        abort(403)

@main.get("/meeting/edit/{id}")
@login_required
def meetingEdit(request: Request, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = session.query(Meetings).filter_by(id=id).first()
    print(meeting.meetingApp)
    if meeting:
        if request.state.user.role == "admin" or request.state.user.id == meeting.teacher_id:
            classname = session.query(Classes).filter_by(id=meeting.class_id).first()
            return render_template(
                "addmeeting.html",
                request = request,
                mon=[], tue=[], wed=[], thu=[], fri=[], sat=[],
                role=request.state.user.role,
                name=request.state.user.first_name,
                classes = session.query(Classes).all(),
                meetingName = meeting.name,
                date = meeting.date,
                className = classname.name,
                meetingHour = str(meeting.hour),
                strings = strings,
                groups=session.query(MeetingGroup).all()
            )
        else:
            abort(403)
    else:
        return render_template("404db.html", request=request, strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@main.get("/approve/{id}")
@login_required
def approveUser(request: Request, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = session.query(User).filter_by(id=id).first()
    if user:
        if (request.state.user.role == "admin"):
            user.confirmed = True
            session.commit()
            return redirect(request.url_for("allUsers"))
        else:
            abort(403)
    else:
        return render_template("404db.html", strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@main.get("/user/settings")
@login_required
def userSettings(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    return templatemanager.TemplateResponse(
        "usersettings.html",
        {
            "request": request,
            "currentPMI": request.state.user.pmi,
            "strings": strings,
            "name": request.state.user.first_name,
            "role": request.state.user.role
        }
    )

@main.post("/user/settings")
@login_required
def userSettingsPost(request: Request, current_user = Depends(manager), pmi: str = Form(...)):
    user = session.query(User).filter_by(id=request.state.user.id).first()
    user.pmi = pmi
    session.commit()
    return redirect(request.url_for("userSettings"))

@main.get("/promote/{role}/{id}")
@login_required
def promoteUser(request: Request, role: str, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = session.query(User).filter_by(id=id).first()
    if user:
        if (request.state.user.role == "admin"):
            if (role == "teacher"):
                user.role = "teacher"
            elif (role == "administrator"):
                user.role = "admin"
            else:
                flash(strings["UNKNOWN_ROLE"])
                return RedirectResponse(request.url_for("allUsers"), status_code=status.HTTP_303_SEE_OTHER)
            session.commit()
            return RedirectResponse(request.url_for("allUsers"), status_code=status.HTTP_303_SEE_OTHER)
        else:
            abort(403)
    else:
        return templatemanager.TemplateResponse(
            "404db.html",
            {
                "request": request,
                "strings": strings,
                "name": request.state.user.first_name,
                "role": request.state.user.role
            }
        )

@main.get("/demote/{id}")
@login_required
def demoteUser(request: Request, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = session.query(User).filter_by(id=id).first()
    if user:
        if (request.state.user.role == "admin"):
            user.role = "student"
            session.commit()
            return redirect(request.url_for("allUsers"))
        else:
            abort(403)
    else:
        return templatemanager.TemplateResponse(
            "404db.html",
            {
                "request": request,
                "strings": strings,
                "name": request.state.user.first_name,
                "role": request.state.user.role
            }
        )

@main.get("/decline/{id}")
@login_required
def declineUser(request: Request, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    user = session.query(User).filter_by(id=id).first()
    if user:
        if (request.state.user.role == "admin"):
            session.delete(user)
            session.commit()
            return RedirectResponse(request.url_for("allUsers"))
        else:
            abort(403)
    else:
        return templatemanager.TemplateResponse(
            "404db.html",
            {
                "request": request,
                "strings": strings,
                "name": request.state.user.first_name,
                "role": request.state.user.role
            }
        )

@main.get("/delete/meeting/{id}")
@login_required
def deleteMeeting(request: Request, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = session.query(Meetings).filter_by(id=id).first()
    print(meeting.teacher_id)
    if meeting:
        if (request.state.user.role == "admin" or request.state.user.id == meeting.teacher_id):
            session.delete(meeting)
            session.commit()
            return redirect(request.url_for("allMeetings"))
        else:
            abort(403)
    else:
        return render_template("404db.html", request=request, strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@main.get("/group/view/{id}")
@login_required
def groupView(request: Request, id: int, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = session.query(Meetings).filter_by(id=id).first()
    classname = session.query(Classes).filter_by(id=meeting.class_id).first()
    print(classname)
    if meeting:
        weeklist = getWeekList(getDate())
        #print(weeklist)
        #print(meeting.date)
        if (meeting.date in weeklist or request.state.user.role == "teacher" or request.state.user.role == "admin"):
            if meeting.group_id:
                print("Meeting has a Group ID")
                meeting = session.query(Meetings).filter_by(date=meeting.date, group_id=meeting.group_id, hour=meeting.hour).all()
                print(meeting[0].group_id)
                return render_template("groupview.html", request=request, meetings=meeting, strings=strings, role=request.state.user.role, name=request.state.user.first_name)
            else:
                return redirect(request.url_for("meetingView"))
        else:
            abort(403)
    else:
        return render_template("404db.html", request=request, strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@main.get("/meeting/view/{id}")
@login_required
def meetingView(request: Request, id: int, continue2: str = None, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    meeting = session.query(Meetings).filter_by(id=id).first()
    classname = session.query(Classes).filter_by(id=meeting.class_id).first()
    print(classname)
    if meeting:
        weeklist = getWeekList(getDate())
        #print(weeklist)
        #print(meeting.date)
        if (meeting.date in weeklist or request.state.user.role == "teacher" or request.state.user.role == "admin"):
            print(continue2)
            if continue2 == "true":
                return render_template(
                    "meetingview.html",
                    request=request,
                    meeting=meeting,
                    strings=strings,
                    name=request.state.user.first_name,
                    role=request.state.user.role,
                    className=classname.name
                )
            if meeting.group_id:
                print("Meeting has a Group ID")
                meeting = session.query(Meetings).filter_by(date=meeting.date, group_id=meeting.group_id, hour=meeting.hour).all()
                return redirect(request.url_for("groupView", id=id))
            else:
                return render_template(
                    "meetingview.html",
                    request=request,
                    meeting=meeting,
                    strings=strings,
                    name=request.state.user.first_name,
                    role=request.state.user.role,
                    className=classname.name
                )
        else:
            abort(403)
    else:
        return render_template("404db.html", request=request, strings=strings, name=request.state.user.first_name, role=request.state.user.role)

@main.post("/meeting/add")
@login_required
def meetingAddPost(request: Request,
                name: str = Form(...), desc: str = Form(""), grading: str = Form(None), mandatory: str = Form(None),
                checking: str = Form(None), confapp: str = Form(...), classname: str = Form(...), date: str = Form(...),
                hour: str = Form(...), urlID: str = Form(None), pmi: str = Form(...), group: str = Form(None), current_user = Depends(manager)):
    if (request.state.user.role == "teacher" or request.state.user.role == "admin"):
        app = confapp
        link = urlID
        """
        print(classname)
        print(date)
        print(pmi)
        print(group)
        """

        lang = getLang().lower()
        strings = getStrings(lang)

        if pmi == "yes":
            if request.state.user.pmi:
                link = request.state.user.pmi
            else:
                #flash(strings["NO_PMI_SET"])
                return redirect(request.url_for("meetingAdd"))

        classID = session.query(Classes).filter_by(name=classname).first()

        if group != "none":
            print("ok, grouped")
            group = session.query(MeetingGroup).filter_by(meetingGroup=group).first().meetingGroup
        else:
            group = None

        ifmeeting = session.query(Meetings).filter_by(date=date, hour=hour, class_id=classID.id).all()
        hmeeting = session.query(Meetings).filter_by(date=date, class_id=classID.id).all()
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

        if index > maximum:
            flash(strings["MAXIMUM_EXCEEDED"])
            return redirect(request.url_for("meetingAdd"))

        if ifmeeting and ifmeeting[0].group_id != group:
            flash(strings["ALREADY_RESERVED"])
            return redirect(request.url_for("meetingAdd"))

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
            teacher_id=request.state.user.id,
            group_id=group
        )

        session.add(new_meeting)
        session.commit()

        return redirect(request.url_for("meetingAdd"))
    else:
        abort(403)

@main.post("/meeting/edit/{id}")
@login_required
def meetingEditPost(
        request: Request,
        id: int,
        name: str = Form(...), desc: str = Form(""), grading: str = Form(None), mandatory: str = Form(None),
        checking: str = Form(None), confapp: str = Form(...), classname: str = Form(...), date: str = Form(...),
        hour: str = Form(...), urlID: str = Form(None), pmi: str = Form(...), group: str = Form(None),
        current_user = Depends(manager)
    ):
    meeting = session.query(Meetings).filter_by(id=id).first()
    if meeting:
        if (request.state.user.role == "teacher" or request.state.user.role == "admin"):
            app = confapp
            link = urlID
            print(classname)
            print(date)
            classid = session.query(Classes).filter_by(name=classname).first()

            ifmeeting = session.query(Meetings).filter_by(date=date, hour=hour, class_id=classid.id).all()
            lang = getLang().lower()
            strings = getStrings(lang)

            if ifmeeting:
                flash(strings["ALREADY_RESERVED"])
                return redirect(request.url_for("meetingAdd"))

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
            
            classID = session.query(Classes).filter_by(name=classname).first()

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
            meeting.teacher_id=request.state.user.id

            session.commit()

            return redirect(request.url_for("meetingAdd"))
        else:
            abort(403)

@main.route("/admin/users")
@login_required
def allUsers(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    if (request.state.user.role == "admin"):
        pending = session.query(User).filter_by(confirmed=False).all()
        users = session.query(User).filter_by(confirmed=True).all()
        return templatemanager.TemplateResponse(
            "allusers.html",
            {
                "request": request,
                "users": users,
                "pendingusers": pending,
                "strings": strings,
                "name": request.state.user.first_name,
                "role": request.state.user.role,
                "current_user": current_user
            }
        )
    else:
        abort(403)

@main.route("/admin/meetings")
@login_required
def allMeetings(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    if (request.state.user.role == "admin"):
        meetings = session.query(Meetings).all()
        return render_template("allmeetings.html", request=request, meetings=meetings, strings=strings, name=request.state.user.first_name, role=request.state.user.role)
    elif (request.state.user.role == "teacher"):
        meetings = session.query(Meetings).filter_by(teacher_id=request.state.user.id).all()
        return render_template("allmeetings.html", request=request, meetings=meetings, strings=strings, name=request.state.user.first_name, role=request.state.user.role)
    else:
        abort(403)

@main.get("/settings")
@login_required
def settings(request: Request, current_user = Depends(manager)):
    lang = getLang().lower()
    strings = getStrings(lang)

    if (request.state.user.role == "admin"):
        return templatemanager.TemplateResponse(
            "settings.html", 
            {
                "request": request,
                "strings": strings,
                "name": request.state.user.first_name,
                "role": request.state.user.role,
                "max": getMax()
            }
        )
    else:
        abort(403)

@main.post("/settings")
@login_required
def settingsPost(request: Request, lang: str = Form(...), maxmeet: int = Form(...), current_user = Depends(manager)):
    if (request.state.user.role == "admin"):
        print(maxmeet)
        max2 = getMax()
        max3 = session.query(Values).filter_by(name="max").first()
        max3.value = str(maxmeet)

        val = session.query(Values).filter_by(name="lang").first()
        val.value = lang
        session.commit()

        r = RedirectResponse(url=request.url_for("settings"), status_code=status.HTTP_303_SEE_OTHER)
        return r
    else:
        abort(403)

"""
@main.app_errorhandler(403)
def error403(e):
    lang = getLang().lower()
    strings = getStrings(lang)

    try:
        name = request.state.user.first_name
    except:
        name = ""

    return render_template("403.html", strings=strings, name=name)
"""
