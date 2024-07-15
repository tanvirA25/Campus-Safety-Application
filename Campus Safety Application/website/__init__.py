from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()
#db_name = "CSA_database"


def app_init():
    app = Flask(__name__)
    # only for the developer
    app.config['SECRET_KEY'] = 'Randompass'
    #app.config['SQLAlchemy_databse_uri'] = f'sqlite:///{db_name}'
    #db.init_app(app)
    
    from.views import pages
    from.authorization import auth
    
    app.register_blueprint(pages, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    
    return app
    