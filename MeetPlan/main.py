from flask import *
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from .models import *
from .dateutil import *

main = Blueprint('main', __name__)

@main.route("/oobe", methods = ['POST', 'GET'])
def oobe():
    #if (request.method == 'POST'):
        #try:
    return render_template("oobe.html")

@login_required
@main.route("/dashboard", methods = ['POST', 'GET'])
def dashboard():
    classname = request.values.get('class')
    print(classname)
    current_date = getDate()
    weeks = getWeekList(current_date)
    if (current_user.role == "admin" or current_user.role == "teacher"):
        isTeacher = "true"
    else:
        isTeacher = "false"
    if classname:
        urnik = Meetings.query.filter_by(className=classname).all()
        print("Urnik")
        print(urnik)
        if urnik:
            return render_template("dashboard.html", name=current_user.first_name, classes=Classes.query.all(), role=current_user.role,
                mon=["", "DKE", "KEM", ""],
                tue=[],
                wed=[],
                thu=[],
                fri=[],
                sat=[],
                dates = weeks,
                isTeacher = isTeacher
            )
        else:
            return redirect(url_for("main.dashboard"))
    else:
        return render_template("dashboard.html", name=current_user.first_name, classes=Classes.query.all(),
        mon=[], tue=[], wed=[], thu=[], fri=[], sat=[], role=current_user.role, dates=weeks, isTeacher=isTeacher
        )

@login_required
@main.route("/class/add", methods=["GET"])
def addClass():
    return render_template("addclass.html", classes = Classes.query.all(), role=current_user.role, name=current_user.first_name)

@login_required
@main.route("/class/add", methods=["POST"])
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
        dates = weeks
    )

@login_required
@main.route("/meeting/add", methods=["GET"])
def meetingAdd():
    return render_template("addmeeting.html", mon=[], tue=[], wed=[], thu=[], fri=[], sat=[], role=current_user.role, name=current_user.first_name, classes = Classes.query.all())

@login_required
@main.route("/meeting/add", methods=["POST"])
def meetingAddPost():
    if (current_user.role == "teacher" or current_user.role == "admin"):
        name = request.form.get('name')
        desc = request.form.get('desc')
        grading = request.form.get('grading')
        mandatory = request.form.get('mandatory')
        checking = request.form.get('checking')
        app = request.form.get('confapp')
        classname = request.form.get('class')

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

        new_meeting = Meetings(class_id=classID.id, required=mandatory, grading=grading, verifying=checking, description=desc, meetingApp=app, name=name, className=classID.name)
        db.session.add(new_meeting)
        db.session.commit()

        return redirect(url_for("main.meetingAdd"))
    else:
        return "<h1>403 Forbidden</h1>", 403

@login_required
@main.route("/settings")
def settings():
    return "", 200