import os
import string
import httpx
import jwt
import bcrypt

from time import time
from random import random, choice
from datetime import timedelta

from fastapi import APIRouter, Request, Depends, Form, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .main import getStrings, getLang
from .functiondeclarations import login_required
from .constants import *

auth = APIRouter()

@manager.user_loader
def query_user(user_id: str):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    return session.query(User).filter_by(email=user_id).first()

def authenticate_user(username: str, password: str):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

@auth.post('/token')
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    token = jwt.encode(user.__dict__, SECRET)

    return {'access_token' : token, 'token_type' : 'bearer'}

@auth.get('/login')
def login(request: Request):
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template('login.html', request=request, strings=strings)

@auth.post('/login')
def login_post(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    lang = getLang().lower()
    strings = getStrings(lang)

    email = data.username
    password = data.password

    user = session.query(User).filter_by(email=email).first()
    if not user:
        print("[login-system] User didn't use e-mail login. Trying to login with username")
        user = session.query(User).filter_by(username=email).first()
        if not user:
            flash(strings["USER_NOT_EXISTS"])
            return redirect(url_for('auth.login'))

    print("[login-system] User used e-mail login")

    if user.confirmed == True or user.role == "admin":
        p = user.verify_password(password)
        print(p)
        if not p:
            flash(strings["WRONG_PASS"])
            return redirect(request.url_for('login')) # if user doesn't exist or password is wrong, reload the page

        # if the above check passes, then we know the user has the right credentials
        access_token = manager.create_access_token(
            data={'sub': user.email},
            expires=timedelta(days=7)
        )
        #return {'token': access_token}

        response = RedirectResponse(request.url_for("dashboard"), status_code=status.HTTP_303_SEE_OTHER)

        
        manager.set_cookie(response, access_token)
        return response
    else:
        flash(strings["PENDING_VERIFICATION"])
        return redirect(request.url_for("login"))

@auth.get('/start')
def start(request: Request):
    lang = getLang().lower()
    strings = getStrings(lang)

    return render_template('start.html', request=request, strings=strings)

@auth.post('/start')
def start_post(request: Request, email: str = Form(...), uname: str = Form(...), fname: str = Form(...), lname: str = Form(...), psw: str = Form(...)):
    lang = getLang().lower()
    strings = getStrings(lang)

    username = uname
    first_name = fname
    last_name = lname
    password = psw
    active = True

    user = session.query(User).all()
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
        return redirect(request.url_for('auth.start'))

    user = session.query(User).filter_by(email=email).first()
    usernme = session.query(User).filter_by(username=username).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash(strings["USER_EMAIL_EXISTS"])
        return redirect(request.url_for('start'))
    elif usernme: # if a user is found, we want to redirect back to signup page so user can try again
        flash(strings["USER_USERNAME_EXISTS"])
        return redirect(request.url_for('start'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, username=username, first_name=first_name, last_name=last_name,
        password=bcrypt.hash(password), role=role, active=active, confirmed=confirmed)

    session.add(new_user)
    session.commit()

    return redirect(request.url_for('login'))

@auth.route('/logout')
@login_required
def logout(request: Request, current_user = Depends(manager)):
    response = redirect(request.url_for('login'))
    response.delete_cookie("login")
    return response

"""
@auth.route('/profile', methods=['POST'])
def profile_update(request: Request):
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
    user = User.query.filter_by(id=request.state.user.id).first()
    user.first_name = first_name
    user.username = username
    user.last_name = last_name
    user.email = email
    if check_password_hash(user.password, old_password):
        user.password = generate_password_hash(new_password, method='sha256')
    db.session.commit()

    return redirect(request.url_for('main.profile'))"""