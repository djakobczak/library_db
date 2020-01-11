from flask import Blueprint, render_template

# !TODO exception is raised when in database is stored uncrypted password and user tries to login
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html')
