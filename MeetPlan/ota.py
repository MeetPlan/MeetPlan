import os
import httpx
import subprocess

from fastapi import APIRouter, Request, Depends
from werkzeug.security import check_password_hash

from .functiondeclarations import *
from .constants import *
from .models import *
from .tableutil import *
from .main import getLang, getStrings

ota = APIRouter(
    tags=["ota"]
)

@ota.get("/update")
@login_required
def update(request: Request, current_user = Depends(manager)):
    if request.state.user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)
        r = httpx.get("https://api.github.com/repos/MeetPlan/MeetPlan/releases")
        print(r.json()[0])
        return render_template("ota.html", request=request, release=r.json()[0], strings=strings, role=request.state.user.role, name=request.state.user.first_name)
    else:
        abort(403)

@ota.post("/update")
@login_required
def updatePost(request: Request, current_user = Depends(manager)):
    if request.state.user.role == "admin":
        lang = getLang().lower()
        strings = getStrings(lang)
        process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
        output = process.communicate()[0].decode()
        print(output)
        if ('up to date' in output):
            print("UP TO DATE")
            flash(strings["UP_TO_DATE"])
            return redirect(request.url_for("update"))
        elif ("Updating" in output):
            flash(strings["UPDATE_SUCCESSFUL"])
            return redirect(request.url_for("update"))
        #return render_template("ota.html", release=r.json()[0], strings=strings)
    else:
        abort(403)