import os
from MeetPlan import db, create_app

if os.path.exists("MeetPlan/db.sqlite"):
    os.remove("MeetPlan/db.sqlite")

app = create_app()
ctx = app.app_context()
ctx.push()

db.create_all(app=app)

ctx.pop()