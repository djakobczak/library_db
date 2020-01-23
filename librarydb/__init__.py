from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from librarydb.config import Config


app = Flask(__name__)
app.config['SECRET_KEY'] = '31e6ce550f73e318b95cfe6513a2a2d6'
POSTGRES_USER = 'postgres'
POSTGRES_PW = 'root'
POSTGRES_URL = '127.0.0.1:5432'
POSTGRES_DB = 'library_final'
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,
                                                               pw=POSTGRES_PW,
                                                               url=POSTGRES_URL,
                                                               db=POSTGRES_DB)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # silence the deprecation warning
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'  # function name of route, set for login required sites
login_manager.login_message_category = 'info'

from librarydb.users.routes import users
from librarydb.books.routes import books
from librarydb.main.routes import main
app.register_blueprint(users)
app.register_blueprint(books)
app.register_blueprint(main)

