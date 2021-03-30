import os
from time import time
from MeetPlan import db, create_app
from MeetPlan.models import User
from werkzeug.security import generate_password_hash

app = create_app()
ctx = app.app_context()
ctx.push()

db.create_all(app=app)

ctx.pop()