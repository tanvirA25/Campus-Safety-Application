from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/logout')
def logout():
    return "<p>logout</p>"

@auth.route('/', methods=['GET','POST'])
def login_page():
    if request.method == 'POST':
        email = request.form.get('email')
        pass1 = request.form.get('password') 
        
        # Debug prints
        print(f"Email from form: {email}")
        print(f"Password from form: {pass1}")

        user = User.query.filter_by(email=email).first()
        # Debug print
        print(f"User found in database: {user}")

        if user:
            if check_password_hash(user.password, pass1):
                flash('Login is successful', category='success')
                return redirect(url_for('pages.home_page'))
            else:
                flash('Password is incorrect', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html")

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
  
            flash('Account Succesfully Created', category='success')
            return redirect(url_for('auth.login_page'))
        
        
    return render_template("sign_up.html")

