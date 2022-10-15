from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager #login manager helps to manage all login related things
#initialize a database
db = SQLAlchemy()
DB_NAME= "database.db"

def create_app():
    # Construct core application
    app = Flask(__name__)
    app.secret_key = 'aanshkotian'
    app.config['Secret Key'] = 'hsdjshjkdhsjk'


    # need to tell flask that we are using this database and where the database is located
    #the SQL alchemy database is located at this location, stores the database in the website folder
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)


    from .views import views #imports variable views from the python package views within the same website folder\
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    
    #import the classes User from models (in the same folder)
    from .models import User
    from .models import Note
    from .models import Reminder
    
    create_database(app) #create our database upon initialization of website

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #where do we go if the user is not logged in, where should flask redirect us if there is a login required 
    login_manager.init_app(app)#tell login manager the name of our app

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #similar to filter_by except it looks for the primary key and check if its equal to whatever we passed (the integer of the id), telling flask what user we are looking for and reference them by their id

    return app

#create our database
#its going to check if the database already exists and if it doesn't its going to create it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app) #need to tell SQLalchemy which app we are creating the database for
        print('Created Database')


def run():
    app = create_app()

    bool = True

    if bool:
        app.run(debug = True)

