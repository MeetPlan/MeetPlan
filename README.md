<!-- This is a test comment -->

# MeetPlan
Plan Zoom, Google Duo, Skype, Teams... meetings

This is an FastAPI app meant especially for schools. It is inspired by Corona-Home schooling and is ultra safe and customized to needs of the school

## IMPORTANT NOTE
### App has recently been migrated to FastAPI. It might be buggy, but otherwise it should work.

# Translations
Translations are held in `MeetPlan/static/langs` folder. You can translate them if you want.

# How to run
It is simple. First install all dependencies using command:
```
pip install -r requirements.txt
```
Then start FastAPI app using following command:
```
uvicorn MeetPlan:app --reload
```
You should see your app at http://127.0.0.1:8000/

# Screenshots

## Add a meeting:
![Add a meeting](https://github.com/mytja/MeetPlan/blob/main/MeetPlan/screenshots/addmeeting.PNG)

## All users:
![All users](https://github.com/mytja/MeetPlan/blob/main/MeetPlan/screenshots/allusers.PNG)

## Dashboard:
![Dashboard](https://github.com/mytja/MeetPlan/blob/main/MeetPlan/screenshots/dashbiard.PNG)

## Meeting details:
![Meeting details](https://github.com/mytja/MeetPlan/blob/main/MeetPlan/screenshots/details.PNG)

## Meetings:
![Meetings](https://github.com/mytja/MeetPlan/blob/main/MeetPlan/screenshots/meetings.PNG)

# Special thanks to:
## Webapp and serving
- [Sebastián Ramírez](https://github.com/tiangolo/) for [FastAPI](https://github.com/tiangolo/fastapi)
- [MushroomMaula](https://github.com/MushroomMaula) for [FastAPI-Login](https://github.com/MushroomMaula/fastapi_login)
- [encode](https://github.com/encode) for [uvicorn](https://github.com/encode/uvicorn)

## Database
- [SQLAlchemy](https://www.sqlalchemy.org/) for [SQLAlchemy](https://www.sqlalchemy.org/)

## Cryptography and security
- [José Padilla](https://github.com/jpadilla) for [PyJWT](https://github.com/jpadilla/pyjwt)
- [Python Cryptographic Authority](https://github.com/pyca) for [bcrypt](https://github.com/pyca/bcrypt/)
- [Python](https://foss.heptapod.net/python-libs) for [passlib](https://foss.heptapod.net/python-libs/passlib)

## Templating engine and file serving
- [Pallets](https://github.com/pallets) for [Jinja2](https://github.com/pallets/jinja)
- [Tin Tvrtković](https://github.com/Tinche) for [aiofiles](https://github.com/Tinche/aiofiles)

## HTTP requests library
- [encode](https://github.com/encode) for [httpx](https://github.com/encode/httpx)

## CSS and design libraries:
- [FontAwesome](https://fontawesome.com/) for their amazing library with icons
- [W3schools](https://w3schools.com/) for their amazing W3.CSS library
