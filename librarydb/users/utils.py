# reservation for 3 days?
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text

from librarydb import db
from librarydb.models import Ksiazki, Rezerwacje, Wypozyczenia


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
        d = {'ksiazka_id': res[0], 'tytul': res[1], 'data_rezerwacji': res[2]}
        rbooks_list.append(d)

    return rbooks_list


def user_borrowed_books(uid):
    """
    Returns list of borrowed books by user whose id is equel uid.
    :param db:      (object)    : database instance
    :param uid:     (int)       : user id
    :return:        (list)      : list of books (title, borrow_date)
    """

    query = text("""
    SELECT 
        w.uzytkownik_id, k.tytul, w.data_wypozyczenia, w.id
    FROM
        wypozyczenia w INNER JOIN 
        egzemplarze e ON e.id = w.egzemplarz_id INNER JOIN
        ksiazki k ON k.id = e.ksiazka_id
    WHERE 
        w.data_oddania IS NULL AND
        w.uzytkownik_id=:uid
    ;   
    """)
    result = db.engine.execute(query, uid=uid).fetchall()

    return result


def get_penalties(db, uid):
    query = text("""
    SELECT 
        egzemplarz_id, tytul, typ_kary, wysokosc, ksiazka_id 
    FROM    
        v_kary_nieoplacone
    WHERE 
        uzytkownik_id=:uid
    """)

    penalties = db.engine.execute(query, uid=uid).fetchall()

    penalties_list = []
    for res in penalties:
        d = {'copyid': res[0], 'title': res[1], 'pen_type': res[2], 'amount': res[3], 'pid': res[4]}
        penalties_list.append(d)

    return penalties_list


def update_user_information(db, user, form):
    user.imie = form.name.data
    user.nazwisko = form.surname.data
    user.pesel = form.pin.data
    user.email = form.email.data
    user.adres = form.address.data
    user.nazwa_uzytkownika = form.username.data
    user.biblioteka_id = form.library_id.data

    try:
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        return False


# sqlalchemy engine execute transaction !TODO
def cancel_penalty_db(db, uid, pid):
    """
    :param db:
    :param uid:     (ind)   : user id
    :param pid:     (int)   : penalty id
    :return:
    """
    query = text("""
    DELETE FROM kary WHERE id=:pid AND uzytkownik_id=:uid
    """)

    db.engine.execute(query, uid=uid, pid=pid)


def pay_penalty_db(db, pid):
    """
    Marks that penalty of id equals pid was paid.
    :param db:      (object)
    :param pid:     (int)   : penalty id
    :return:
    """
    query = text("""
        INSERT INTO platnosci (id_kary, data_platnosci) VALUES (:pid, :timestamp);
    """)
    db.engine.execute(query, pid=pid, timestamp=datetime.now())


def get_payments(db, uid):
    query = text(
        """
        SELECT * FROM v_platnosci WHERE user_id=:uid
        """
    )
    payments = db.engine.execute(query, uid=uid).fetchall()

    payments_list = []
    for pay in payments:
        d = {'pid': pay[0], 'pay_date': pay[1], 'title': pay[4], 'pen_type': pay[5], 'eid': pay[6], 'amount': pay[7]}
        payments_list.append(d)

    return payments_list

def return_book_db(lend_id):
    bbook = Wypozyczenia.query.get(lend_id)
    bbook.data_oddania = datetime.now()

    return commit_changes()


def commit_changes():
    try:
        db.session.commit()
        return True
    except IntegrityError as e:
        print(str(e))
        db.session.rollback()
        return False