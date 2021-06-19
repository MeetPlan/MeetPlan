# models.py

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from passlib.hash import bcrypt

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = Column(String(100), unique=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    pmi = Column(String(100))
    role = Column(String(100))
    active = Column(Boolean)
    confirmed = Column(Boolean)
    meetings = relationship('Meetings', backref='user', lazy=True)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    meetings_classes = relationship('Meetings', backref='classes', lazy=True)

class MeetingGroup(Base):
    __tablename__ = "meetinggroup"

    id = Column(Integer, primary_key=True)
    meetingGroup = Column(String(100))
    meetings = relationship('Meetings', backref='meetinggroup', lazy=True)

class Meetings(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    date = Column(String(100))
    hour = Column(Integer)
    required = Column(Boolean)
    grading = Column(Boolean)
    verifying = Column(Boolean)
    description = Column(Text())
    meetingApp = Column(String(100))
    link = Column(String(1000))
    teacher_id = Column(Integer)
    name = Column(String(100))
    meetingGroup = Column(String(100))
    class_id = Column(Integer, ForeignKey(Classes.id))
    teacher_id = Column(Integer, ForeignKey(User.id))
    group_id = Column(Integer, ForeignKey(MeetingGroup.id))

class Values(Base):
    __tablename__ = "values"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    value = Column(String(1000))
