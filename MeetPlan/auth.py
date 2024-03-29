from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, login_fresh, current_user
from .models import User
from time import time
from random import random, choice
from . import db
from .main import getStrings, getLang
import requests
import os
import string
import httpx

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template('login.html', strings=strings)

@auth.route('/login', methods=['POST'])
def login_post():
    lang = getLang().lower()
    strings = getStrings(lang)

    email = request.form.get('uname')
    password = request.form.get('psw')

    user = User.query.filter_by(email=email).first()
    if not user:
        print("[login-system] User didn't use e-mail login. Trying to login with username")
        user = User.query.filter_by(username=email).first()
        if not user:
            flash(strings["USER_NOT_EXISTS"])
            return redirect(url_for('auth.login'))

    print("[login-system] User used e-mail login")

    if user.confirmed == True or user.role == "admin":

        # check if user actually exists
        # take the user supplied password, hash it, and compare it to the hashed password in database
        if not check_password_hash(user.password, password):
            flash(strings["WRONG_PASS"])
            return redirect(url_for('auth.login')) # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        login_user(user)
        return redirect(url_for('main.dashboard'))
    else:
        flash(strings["PENDING_VERIFICATION"])
        return redirect(url_for("auth.login"))

@auth.route('/start')
def start():
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template('start.html', strings=strings)

@auth.route('/start', methods=['POST'])
def start_post():
    lang = getLang().lower()
    strings = getStrings(lang)

    email = request.form.get('email')
    username = request.form.get('uname')
    first_name = request.form.get('fname')
    last_name = request.form.get('lname')
    password = request.form.get('psw')
    active = True

    user = User.query.all()
    if (user):
        role = "student"
    else:
        role = "admin"

    if (role == "admin"):
        confirmed = True
    else:
        confirmed = False

    if email == "" or first_name == "" or last_name == "" or password == "":
        flash(strings["ALL_FIELDS"])
        return redirect(url_for('auth.start'))

    user = User.query.filter_by(email=email).first()
    usernme = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash(strings["USER_EMAIL_EXISTS"])
        return redirect(url_for('auth.start'))
    elif usernme: # if a user is found, we want to redirect back to signup page so user can try again
        flash(strings["USER_USERNAME_EXISTS"])
        return redirect(url_for('auth.start'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, username=username, first_name=first_name, last_name=last_name,
        password=generate_password_hash(password, method='sha256'), role=role, active=active, confirmed=confirmed)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

"""
@auth.route('/profile', methods=['POST'])
def profile_update():
    email = request.form.get('email')
    username = request.form.get('uname')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')

    # if email == "" or first_name == "" or last_name == "" or password == "":
    #     flash('Potrebno je izpolniti vsa polja!')
    #     return redirect(url_for('auth.start'))
    #
    # user = User.query.filter_by(email=email).first()
    # usernme = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database
    #
    # if user: # if a user is found, we want to redirect back to signup page so user can try again
    #     flash('Uporabnik_ca s tem elekronskim naslovom že obstaja.')
    #     return redirect(url_for('auth.start'))
    # elif usernme: # if a user is found, we want to redirect back to signup page so user can try again
    #     flash('Uporabnik_ca s tem uporabniškim imenom že obstaja.')
    #     return redirect(url_for('auth.start'))

    #new_user = User(email=email, first_name=first_name, last_name=last_name, terms_accepted= terms_accepted, password=generate_password_hash(password, method='sha256'))


    #db.session.profile_update(new_user)
    print(username)
    user = User.query.filter_by(id=current_user.id).first()
    user.first_name = first_name
    user.username = username
    user.last_name = last_name
    user.email = email
    if check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password, method='sha256')
    db.session.commit()

    return redirect(url_for('main.profile'))"""