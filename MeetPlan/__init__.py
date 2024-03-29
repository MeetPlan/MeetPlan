# init.py
import os
import platform

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    passf = open("pass.txt")

    app.config['SECRET_KEY'] = passf.read()
    passf.close()

    load_dotenv()
    docker = os.getenv("DOCKER")
    if docker == "true":
        print("Using Docker database")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////db/db.sqlite'
    else:
        print("Using Local database")
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    # login_manager.login_message = "Please log in to access this page."
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for auth routes in our app
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for non-auth parts of app
    from .db import db as db_blueprint
    app.register_blueprint(db_blueprint)

    # blueprint for non-auth parts of app
    from .ota import ota as ota_blueprint
    app.register_blueprint(ota_blueprint)

    return app
