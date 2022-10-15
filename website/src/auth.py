import email

from flask import Blueprint
from flask import Flask, render_template, url_for, redirect, request, session, jsonify, flash, Blueprint


from . import db
#import the user class
from .models import User

#import wrkzeug from flask_login that allows us to hash a password (allow us to store the password thats not in plain text)
#what is a hashing function? A hashing function is a one-way function (it doesn't have an inverse)
#x --> y, y--> ? 

from werkzeug.security import generate_password_hash,check_password_hash

from flask_login import login_user,login_required,logout_user,current_user, user_logged_in

auth = Blueprint("auth",__name__) #different views



@auth.route('/login',methods = ['POST','GET'])
def login():
    if request.method =='POST':
        #get the information from the form
        
        # email = request.form.get('email')

        username = request.form.get('userName') #there is no username to access because there is no username inputted in the form
        password = request.form.get('password')
        
        
        #need to check the database to see if its a valid email and password
        #filter all of the users by the email inputted
        #'User' is the name of the database
        
        user = User.query.filter_by(username=username).first() #returns the first result, should only have 1 since each user should have a unique email
        if user:
            #check if password typed in is equal to the hash stored on the server
            if check_password_hash(user.password,password): #it will hash the inputted password then check it against user.password
                name = username
                
                flash(f'Logged in successfully as {name}!',category = 'success')


                #login user
                login_user(user,remember=True) #remembers the fact that the user is logged in until the user clears their browsing history/session, if web server is running it remembers the user
                return redirect(url_for('views.home')) #return to home page
            else:
                flash('Incorrect username or password',category ='error')
        else:
            flash('Username does not exist',category = 'error')

    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required #cannot access logout route/page unless the user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login')) #bring back to login page

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('userName')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first() #returns the first result, should only have 1 since each user should have a unique email
        user1 = User.query.filter_by(username=username).first()
        if user: #if user exists in the database already state that there is an error
            flash('Email already exists.',category = 'error')
        elif user1:
            flash('Username already taken.',category = 'error')
        elif len(email) < 4:
            flash("Email must be greater than 3 characters", category = "error")
        elif len(username) < 3:
            flash("Username must be greater than 2 characters")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 characters", category = "error")
        elif password1 != password2:
            flash("Passwords do not match", category = "error")
        elif len(password1) < 7:
            flash("Password must be atleast 7 characters", category = "error")
        else:
            #add user to database
            new_user = User(email=email,username=username,first_name=first_name,password=generate_password_hash(password1,method='sha256'))#'sha256' is a hashing algorithm
            db.session.add(new_user) #this adds a new user to the database
            db.session.commit() #have to put this after u add the user to the database
            login_user(new_user,remember = True) #login the user after he successfully creates an account
            flash("Account created!", category = "success")
            return redirect(url_for('views.home')) #after the user signs up we want to redirect them to the home page, views is the name of our blueprint and home is the name of our function, so the computer finds what url maps to the home function, note that one could just put in a '/' and it will work the same but if you ever change the url for the home function we will have to update this redirect function 

    return render_template("sign_up.html",user=current_user)
