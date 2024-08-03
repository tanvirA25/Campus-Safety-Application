from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import db
import sqlite3
from sqlalchemy import cast,func
from .models import Feedback, User, Report
from datetime import date, datetime, timedelta
from .alert import send

pages = Blueprint('pages', __name__)

# Gets the information from the database to show alerts in home page
@pages.route('/home', methods=['GET'])
@login_required
def home_page():
    
    if request.method == "GET":
        all = Report.query.all()  
        
        # if number of alerts in database exceeds 40 deletes any entries before 5 days ago
        if len(all) > 40:
            range_date = datetime.now() - timedelta(days=5)
            
            before_date = Report.query.filter(Report.time <= range_date)
            all_prev = before_date.all()
            for entries in all_prev:
                db.session.delete(entries)
            db.session.commit()
            
        
        todays_date = date.today()
        # queries todays alerts
        today = Report.query.filter(func.date(Report.time) == todays_date).order_by(Report.id.desc()).all()
           # queries for alerts not today
        other = Report.query.filter(func.date(Report.time) != todays_date).order_by(Report.id.desc()).limit(5)
        # if admin show id else no
        if (current_user.admin()):
            return render_template("home.html", user=current_user, today=today, other=other, admin=True)
        else:
            return render_template("home.html", user=current_user, today=today, other=other, admin=False)
            

@pages.route('/account', methods=['GET'])
@login_required
def account_page():
    # for account gets the info of user from the database
    if request.method == 'GET':
        user_id = current_user.id
        user_info = User.query.filter_by(id=user_id).first()
        
        # if user is admin then show all user info without passwords
        if (current_user.admin()):
            result = User.query.all()
            return render_template("account.html", user=current_user, account_page=result, admin=True)
        else:
            return render_template("account.html", user=current_user, account_page=user_info, admin=False)

@pages.route('/report', methods=['GET','POST'])
@login_required
def incident_report_page():
    
    # gets all the information from the user and then commits to the database
    if request.method == 'POST':
        title = request.form.get('alert-title')
        level = request.form.get('alert-level')
        time = request.form.get('alert_time')
        convert_time = datetime.strptime(time, '%Y-%m-%dT%H:%M')
        location = request.form.get('alert_location')
        short_description = request.form.get('short_descp')
        long_description = request.form.get('long_descp')
        
    
        # condition to flash error message if not valid inputs else commit and send users email
        if len(long_description) < 3:
            flash("Too small for a long description.", category='error')
        elif len(short_description) < 3:
             flash("Too small for a short description.", category='error')
        else:
            new_report = Report(title=title, level=level, location=location, time=convert_time,  short_description =short_description, long_description=long_description)
            db.session.add(new_report)
            db.session.commit()
            flash("Report is succesfully added")
            send()
            flash("Report is succesfully send to all user")
            
    
    return render_template("report.html", user=current_user)


@pages.route('/feedback', methods=['GET','POST'])
@login_required
def feedback_page():
    
     # gets information from the database of all feedback if user is admin
    if request.method == 'GET':
        if (current_user.admin()):
            result = Feedback.query.all()
            return render_template("feedback.html", user=current_user, feedback_page=result, admin=True)
        
     # else get the input
    if request.method == 'POST':
        feedback = request.form.get('feedback')
        rating = request.form.get('rating')
        
        # condition to check if the feedback is too short else commit to the database
        if len(feedback) < 3:
            flash("Too small of a feedback.", category='error')
        else:
            new_feedback = Feedback(feedback=feedback, rating=rating, user_id=current_user.id)
            db.session.add(new_feedback)
            db.session.commit()
            flash("Feedback is succesfully added", category='success')
   
        
    
    return render_template("feedback.html", user=current_user)



@pages.route('/delete_feedbacks', methods=['GET','POST'])
@login_required
def delete_feedbacks():
    
     # if user is admin show have the ability to delete feedbacks 
    if (current_user.admin()):
        all_feedbacks = Feedback.query.all()
        for entries in all_feedbacks:
            db.session.delete(entries)
        db.session.commit()
        flash("All feedbacks has been deleted", category="success")
        return redirect(url_for('pages.feedback_page'))
