from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


import sqlite3
from sqlite3 import Error
from datetime import datetime
import time



class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note') 
    reminder = db.relationship('Reminder')



class Reminder(db.Model):
    id = db.Column(db.Integer,primary_key = True)

    # need a column for text and date for reminder
    data = db.Column(db.String(1000))
    date_create = db.Column(db.DateTime(timezone=True),default=func.now())
    
    # also need a column for when the user wants the reminder to send
    """we will ask the user to choose a date e.g. Feb 5th 2022, this date will be represented as an integer - 020522"""
    date_reminder = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# class MSG_Database(db.Model):
#     id = db.Column(db.Integer,primary_key = True)




# class Reminder():


