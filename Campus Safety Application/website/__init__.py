from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd
from flask_login import LoginManager


db = SQLAlchemy()
db_name = "CSA_database.db"

# app create with database
def app_create():
    app = Flask(__name__)
    # only for the developer secret key for database
    app.config['SECRET_KEY'] = 'djdjjdj djjdjdjd '
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(getcwd(),"website", db_name)}'
    db.init_app(app)

    # uses the pages in authorization and views to create pages for the app
    from.views import pages
    from.authorization import auth

    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User
    
    database_creation(app)
    
    # login manager 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)
    
    # gets the user id for login manager 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
       

    return app

# creates the database if it doesn't exist
def database_creation(app):
    if not path.exists('website/' + db_name):
        with app.app_context():
            db.create_all()
            print('database created')
            

