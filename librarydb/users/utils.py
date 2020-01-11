
# reservation for 3 days?
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

from librarydb.models import Ksiazki, Rezerwacje


def reserved_books_by_user(db, user_id):
    """
    Returns copies of books currently reserved by user.
    :param db:          (object)    : db instance
    :param user_id:     (int)       : user id
    :return:
    """
    query = f"""
    SELECT 
	    k.id, k.tytul, r.data_rezerwacji
    FROM
        rezerwacje r INNER JOIN 
        ksiazki k ON r.ksiazka_id=k.id
    WHERE r.uzytkownik_id={user_id}
    ;
    """
    result = db.engine.execute(query).fetchall()
    return result


def reserved_books_by_user_alchemy(db, uid):
    rbooks = db.session.query(Ksiazki.id, Ksiazki.tytul, Rezerwacje.data_rezerwacji) \
        .join(Ksiazki, Rezerwacje.ksiazka_id == Ksiazki.id) \
        .filter(Rezerwacje.uzytkownik_id == uid).all()

    rbooks_list = []
    for res in rbooks:
        d = {}
        d['ksiazka_id'] = res[0]
        d['tytul'] = res[1]
        d['data_rezerwacji'] = res[2]
        rbooks_list.append(d)

    return rbooks_list


def user_borrowed_books(db, uid):
    """
    Returns list of borrowed books by user whose id is equel uid.
    :param db:      (object)    : database instance
    :param uid:     (int)       : user id
    :return:        (list)      : list of books (title, borrow_date)
    """

    query = f"""
    SELECT 
        w.uzytkownik_id, k.tytul, w.data_wypozyczenia
    FROM
        wypozyczenia w INNER JOIN 
        egzemplarze e ON e.id = w.egzemplarz_id INNER JOIN
        ksiazki k ON k.id = e.ksiazka_id
    WHERE 
        w.data_oddania IS NULL AND
        w.uzytkownik_id={uid}
    ;   
    """
    result = db.engine.execute(query).fetchall()
    return result


def update_user_information(db, user, form):
    user.imie = form.name.data
    user.nazwisko = form.surname.data
    user.pesel = form.pin.data
    user.email = form.email.data
    user.adres = form.address.data
    user.nazwa_uzytkownika = form.username.data

    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False





