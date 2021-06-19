# init.py
from .models import *
from .constants import *

from .auth import auth
from .main import main
from .ota import ota
from .db import db

app.include_router(auth)
app.include_router(main)
app.include_router(ota)
app.include_router(db)