from flask import Blueprint, render_template


pages = Blueprint('pages', __name__)




@pages.route('/home', methods=['GET','POST'])
def home_page():
    return render_template("home.html")



