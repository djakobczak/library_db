from sqlalchemy.sql import func
from librarydb.models import Ksiazki, Rezerwacje, Wypozyczenia, Egzemplarze


# Model.query is a shortcut to db.sesssion.query(model) it's not callable.
# If you're not querying a model, continue to use db.session.query(...)
# available_books = db.session.query(func.count(Egzemplarze.id))\
#     .filter(Egzemplarze.ksiazka_id == book_id)\
#     .join(Wypozyczenia, (Wypozyczenia.egzemplarz_id == Egzemplarze.id))
# reservations = db.session.query(func.count(Rezerwacje.id)) \
#     .filter(Rezerwacje.ksiazka_id == book_id).first()


# print(reservations)
# available_books = db.session.query(func.count(Egzemplarze.id)) \
#     .filter(Egzemplarze.ksiazka_id == book_id).all()
# print(available_books)
# abooks = db.session.query(func.public.v_ksiazki_dostepne()).first()       # how to call function


def available_books(db, book_id):
    """
    Count number of available copies i.e. copies of books that are neither
    reserved nor borrowed
    :param db:      (object)    : db instance
    :param book_id: (int)       : book id
    :return:        (int)       : number of copies that can be reserved or borrowed
    """
    query = f"""
    SELECT
    (COUNT(*)-(SELECT COUNT(*) FROM rezerwacje WHERE ksiazka_id={book_id})) AS ksiazki_dostepne
    FROM
        egzemplarze e
    WHERE
	    ksiazka_id={book_id} AND
	    e.id NOT IN (SELECT egzemplarz_id FROM wypozyczenia WHERE data_oddania IS NULL)
    ;
    """
    result = db.engine.execute(query).scalar()
    return result