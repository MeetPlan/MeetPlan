FROM python:3.7-buster

COPY . /app
WORKDIR /app

RUN apt update -y && \
    apt upgrade -y && \
    apt install -y sqlite3 libsqlite3-dev gunicorn3

RUN python3.7 -m venv /venv
RUN /venv/bin/python -m pip install -r requirements.txt

# Generate random password (only used for login - not for hashing)
RUN openssl rand -base64 30 > pass.txt

EXPOSE 80

CMD /venv/bin/python createdockerdb.py && /venv/bin/python -m gunicorn -w 4 -b 0.0.0.0:80 "MeetPlan:create_app()"

# Used for debugging
#CMD bash
