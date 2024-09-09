from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import datetime

# database for feedback with id, date, rating, and feedbacks, user_id
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    rating = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='feedback')

# database for User with id, email, password, firstname, lastname 
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(320), unique=True)
    password = db.Column(db.String(20))
    fname = db.Column(db.String(25))
    lname = db.Column(db.String(25))
    feedback = db.relationship('Feedback', back_populates='user')
    
    # fucntion to check if user is admin
    def admin(self):
        return self.email.startswith("admin")
    
# database for Report with id, title, level, date time, location, descripotion
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10000))
    level = db.Column(db.String(1000))
    time = db.Column(db.DateTime, nullable = False) 
    location = db.Column(db.String(1000))
    short_description = db.Column(db.String(1000))
    long_description = db.Column(db.String(20000))
    
    
    
    
    