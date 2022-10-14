from flask_login import login_required,current_user#current_user gives us all information about the current user, if user is not logged in it states that user is an anonymous user and unauthenticated 

from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint #importing the render template function 


from . import db 
from .models import Note, Reminder

import json



views = Blueprint('views', __name__)

# **Note:You can stack decorators**
#define a views/ root
#decorator @views.route whenever our url ends with / it will match it to the argument passed through the decorator and take us to the home page
@views.route('/',methods=['POST','GET'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("home.html",user= current_user) #renders the home.html template, check if user is authenticated


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/about')
def about():
    return render_template("about.html",user=current_user)

 
@views.route('/contact-us')
def contact_us():
    return render_template("contact_us.html",user=current_user)


@views.route('/schedule',methods = ['POST','GET'])
@login_required
def schedule():
    if request.method == 'POST':
        reminder = request.form.get('reminder')
        if len(reminder) < 1:
            flash('Note is too short!', category='error')
        else:
            new_reminder = Reminder(data=reminder, user_id=current_user.id)
            db.session.add(new_reminder)
            db.session.commit()
            flash('Reminder added!', category='success')

    return render_template("cal.html")