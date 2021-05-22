from flask import *
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from .models import *
from .tableutil import *
from .main import getLang, getStrings
from werkzeug.security import check_password_hash
import os
import httpx
import subprocess

ota = Blueprint('ota', __name__)

@ota.route("/update", methods=["GET"])
@login_required
def update():
    if current_user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)
        r = httpx.get("https://api.github.com/repos/MeetPlan/MeetPlan/releases")
        print(r.json()[0])
        return render_template("ota.html", release=r.json()[0], strings=strings, role=current_user.role, name=current_user.first_name)
    else:
        abort(403)

@ota.route("/update", methods=["POST"])
@login_required
def updatePost():
    if current_user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)
        process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
        output = process.communicate()[0].decode()
        print(output)
        if ('up to date' in output):
            print("UP TO DATE")
            flash(strings["UP_TO_DATE"])
            return redirect(url_for("ota.update"))
        elif ("Updating" in output):
            flash(strings["UPDATE_SUCCESSFUL"])
            return redirect(url_for("ota.update"))
        #return render_template("ota.html", release=r.json()[0], strings=strings)
    else:
        abort(403)