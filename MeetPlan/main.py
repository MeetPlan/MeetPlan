from flask import *
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from .models import *

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
    if classname:
        urnik = Meetings.query.filter_by(className=classname).all()
        if urnik:
            return render_template("dashboard.html", name=current_user.first_name, classes=["1b", "2b", "3a"],
                mon=["", "DKE", "KEM", ""],
                tue=[],
                wed=[],
                thu=[],
                fri=[],
                sat=[]
            )
        else:
            return render_template("dashboard.html", name=current_user.first_name, classes=["1b", "2b", "3a"],
                mon=[],
                tue=[],
                wed=[],
                thu=[],
                fri=[],
                sat=[]
            )
    else:
        return render_template("dashboard.html", name=current_user.first_name, classes=["1b", "2b", "3a"],
        mon=[], tue=[], wed=[], thu=[], fri=[], sat=[]
        )
