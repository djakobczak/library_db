import psycopg2
from psycopg2.errors import lookup
from flask import g
# from librarydb.models import create_book


# maybe wrap all db function into a class -> it will solve the problem with naming

GOOD_ANS = 'OK'


def connect_db(return_cur=True):
    conn = psycopg2.connect(
        host="localhost",
        database="library",
        user="postgres",
        password="root"
    )
    if return_cur:
        cur = conn.cursor()
        return cur
    else:
        return conn


def get_conn():
    if 'db' not in g:
        g.conn = connect_db(return_cur=False)

    return g.conn


def get_cur():
    """
    Gets connection to database.
    If application context does not contain connection to db then it creates that connection.
    :return:    (obj)   : cursor object of postgresql database
    """
    if 'db' not in g:
        g.cur = connect_db()

    return g.cur


def get_all_books():
    """
    Simple query to get all records from books table.
    :return:        (list)  : list of records returned by calling query
    """
    cur = get_cur()
    query = """SELECT * FROM books"""
    cur.execute(query)
    books = cur.fetchall()
    return books
    # return convert_books_list(books)


def convert_books_list(books):
    """
    Converts list of books to format that is acceptable by jinja2
    :param books:   (list)  : list of tuples that represent books
    :return:        (list)  : list of dictionaries
    """
    cbooks = []
    for book in books:
        # !TODO not sure whether it is good way to do that
        book_dict = {'title': book[1], 'author': book[2], 'category': book[4]}
        cbooks.append(book_dict)
    return cbooks


def add_user(name, surname, pin, email, passwd, is_admin=False):
    """
    Add user to database.
    :param name:
    :param surname:
    :param pin:
    :param email:
    :param passwd:
    :param is_admin:
    :return:
    """
    query = f"""
    INSERT INTO users (name, surname, pin, email, passwd, is_admin)
    VALUES ('{name}', '{surname}', '{pin}', '{email}', '{passwd}', {is_admin});
    """
    conn = get_conn()

    try:
        conn.cursor().execute(query)
        conn.commit()
        return GOOD_ANS

    except psycopg2.errors.lookup("23505") as e:        # UniqueViolation
        print(str(e))
        conn.rollback()
        return "Użytkownik o podanym peselu lub mailu już istnieje"


def get_user(arg, attr='uid'):
    """
    Finds user by specifying uid, pin or email
    :param arg:     (
    :param attr:    (str)   : indicates attribute that is used to filter user
    :return:        (tuple) : represents user record in database
    """
    if attr == 'uid':
        query = f"""
            SELECT * FROM users WHERE id={arg};
            """
    elif attr == 'pin':
        query = f"""
            SELECT * FROM users WHERE pin='{arg}';
            """
    elif attr == 'email':
        query = f"""
            SELECT * FROM users WHERE email='{arg}';
            """
    else:
        return None

    cur = get_cur()
    cur.execute(query)
    return cur.fetchone()

def insert_book(title, author, category, count, description):
    """
    Inserts book to database. Operation will be aborted if book already exists in database.
    :param title:
    :param author:
    :param category:
    :param count:
    :param description:
    :return:
    """
    query = f"""
    INSERT INTO books (title, author, category, count, description)
    VALUES ('{title}', '{author}', '{category}', {count}, '{description}');
    """
    conn = get_conn()
    try:
        conn.cursor().execute(query)
        conn.commit()
        return GOOD_ANS
    except psycopg2.errors.lookup("23505") as e:        # UniqueViolation
        print(str(e))
        conn.rollback()
        return "Taka książką już istnieje w bazie danych"
    except Exception as e:
        print(str(e))
        conn.rollback()
        return "Wystąpił błąd"


def get_book(book_id):
    query = f"""
    SELECT * FROM books WHERE bid={book_id}
    """
    cur = get_cur()
    cur.execute(query)
    return cur.fetchone()


def update_book_db(book_id, title, author, category, count, description):
    """
    Updates book information
    :param book_id:
    :param title:
    :param author:
    :param category:
    :param count:
    :param description:
    :return:
    """
    query = f"""
    UPDATE books 
    SET title='{title}', author='{author}', category='{category}', count={count}, description='{description}'
    WHERE bid={book_id}
    """
    return commit_changes(query)


def commit_changes(query):
    """
    Executes passed query and commit changes to database.
    :param query:   (str)   : psql query
    :return:        (str)   : result of commit
    """
    conn = get_conn()
    try:
        conn.cursor().execute(query)
        conn.commit()
        return GOOD_ANS
    except psycopg2.errors.lookup("23505") as e:  # UniqueViolation
        print(str(e))
        conn.rollback()
        return "Taka książką już istnieje w bazie danych"
    except Exception as e:
        print(str(e))
        conn.rollback()
        return "Wystąpił błąd"


def delete_book_db(book_id):
    """
    Deletes book from database
    :param book_id:     (int)   : book id
    :return:
    """
    query = f"""
    DELETE FROM books WHERE bid={book_id};
    """
    return commit_changes(query)
