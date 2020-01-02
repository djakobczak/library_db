from flask_login import UserMixin
from librarydb.database import get_user
from librarydb import login_manager, db


@login_manager.user_loader
def load_user(uid):
    """

    :param uid:     (int)   : user id
    :return:        (obj)   : User instance
    """
    user = get_user(uid, attr='uid')
    if user:
        return User(*user)
    else:
        return None

def create_user(user_tuple):
    if user_tuple:
        return User(*user_tuple)

def create_book(book_tuple):
    if book_tuple:
        return Book(*book_tuple)

class User(UserMixin):

    # name 'id' is necessary else NotImplemented get_id() exception
    def __init__(self, id, name, surname, pin, email, password, is_admin):
        self.id = id
        self.name = name
        self.surname = surname
        self.pin = pin
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return f"User('{self.name}', '{self.surname}', '{self.email}')"


class Book():

    def __init__(self, bid, title, author, category, count, description):
        self.bid = bid
        self.title = title
        self.author = author
        self.category = category
        self.count = count
        self.description = description

    def __repr__(self):
        return f"Book({self.title}, {self.author}, {self.count})"

class Book2(db.Model):
    __table_args__ = (
        db.UniqueConstraint('title', 'author', name='unique_title_author'),
    )
    __tablename__ = "books"

    bid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    category = db.Column(db.String)
    count = db.Column(db.Integer, db.CheckConstraint('count > -1'), nullable=False)
    description = db.Column(db.Text)
