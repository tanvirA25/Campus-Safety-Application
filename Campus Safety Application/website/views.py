from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)

@pages.route('/')
def home_page():
    return render_template('login.html')