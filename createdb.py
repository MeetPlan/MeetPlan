import os
from time import time
from MeetPlan import db, create_app
from MeetPlan.models import User
from werkzeug.security import generate_password_hash

if os.path.exists("MeetPlan/db.sqlite"):
    os.remove("MeetPlan/db.sqlite")

app = create_app()
ctx = app.app_context()
ctx.push()

db.create_all(app=app)

ctx.pop()