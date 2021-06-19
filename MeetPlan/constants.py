import os

from fastapi import FastAPI, status, Request
from fastapi_login import LoginManager
from starlette.responses import RedirectResponse
from os.path import join, dirname, realpath

from .functiondeclarations import NotAuthenticatedException
from .models import *

MEETPLAN_DB_VERSION = "v1.0"
MEETPLAN_VERSION = "Guinea pig 1.1"
# Guinea pig means the earliest and the most buggy version
# Beta is a little bit more stable release
# v (or Stable) means production ready (although it's never really production ready :sweat_smile:)

app = FastAPI()

operating_directory = os.path.dirname(os.path.abspath(__file__))

#print(operating_directory)

if os.path.exists("secrettoken.txt"):
    f = open(file="secrettoken.txt", mode="r")
    SECRET = f.read()
    f.close()
else:
    rand = os.urandom(24).hex()
    f = open(file="secrettoken.txt", mode="w+")
    f.write(rand)
    f.close()
    SECRET = rand

manager = LoginManager(SECRET, token_url='/login', use_cookie=True)
#print(manager.cookie_name)
manager.cookie_name = 'login'
manager.useRequest(app)
manager.not_authenticated_exception = NotAuthenticatedException

Base.metadata.create_all(bind=engine)

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="MeetPlan/static"), name="static")

tempdir = os.path.join(operating_directory, "templates")
#print(tempdir)

templatemanager = Jinja2Templates(directory=tempdir)

def redirect(url):
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)

def render_template(template, **kwargs):
    return templatemanager.TemplateResponse(template, kwargs)

@app.exception_handler(NotAuthenticatedException)
def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url='/login')

class Flash:
    flashes = []

flashmanager = Flash()

def flash(description):
    flashmanager.flashes.append(description)