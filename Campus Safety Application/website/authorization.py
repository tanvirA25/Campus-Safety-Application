from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# main page for login 
@auth.route('/', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        pass1 = request.form.get('password') 
        # checks if email exist 
        user = User.query.filter_by(email=email).first()

          # checks if email exists and password matches 
          # then login remembers it until browser chache is refreshed
          # after redirect to home page
          # else flash error message
        if user:
            if check_password_hash(user.password, pass1):
                flash('Login is successful', category='success')
                login_user(user, remember=True)
                return redirect(url_for('pages.home_page'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


 # when clicked logouts out the account and redirects to login page
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))


        # gets input from the sign up page commits to database 
        # goes through multiple condition of complexity for valid account creation
        # then redirects to home page
        # else flash error message
@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('college-email')
        fname = request.form.get('first-name')
        lname = request.form.get('last-name')
        password1 = request.form.get('password') 
        con_password = request.form.get('confirm-password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exist, try a different email', category='error')  
        elif len(fname) < 3:
            flash('Name must be at lest 2 characters', category='error')
        elif len(email) < 4:
            flash('Email length is less than 4', category='error')
        elif password1 != con_password:
            flash('Passwords do not match', category='error')
        elif len(password1) < 6:
            flash('Password length less than 6',category='error')
        else:
            new_user = User(email=email, fname = fname, lname=lname, password=generate_password_hash(password1, method='pbkdf2:sha256') )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            
  
            flash('Account Succesfully Created', category='success')
            return redirect(url_for('pages.home_page'))
        
        
    return render_template("sign_up.html", user=current_user)

