from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from librarydb import db
from librarydb.models import Ksiazki, Rezerwacje, Wypozyczenia, Egzemplarze, Autor, Biblioteki
from librarydb.models import TypKary, Kary

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

def get_penalties_types():
    """

    :return: (list) : list of penalties types
    """
    penalties = TypKary.query.all()
    return penalties

def get_libraries_types():
    """
    :return: (list) : list of penalties types
    """
    libraries = Biblioteki.query.all()
    return libraries


def get_penalties_tuples():
    """
    Changing format is necessary to avoid jinja2 exception when indexing inside url_for() method

    :param penatlies:   (list)  : list of list penalties (tuples)
    :return:            (list)  : list of penalties (dict)
    """
    penatlies = get_penalties_types()
    out_pen = []
    for pen in penatlies:
        out_pen.append((str(pen.id), (pen.typ_kary + " - " + str(pen.wysokosc))))
    return out_pen

def get_libraries_tuples():
    libraries = get_libraries_types()

    out_lin = []
    for lib in libraries:
        out_lin.append((str(lib.id), lib.nazwa))
    return out_lin


def add_penalty(db, uid, copyid, pid):
    """
    Add penalty to the user specified by his/her user id.
    :param db:
    :param uid:
    :param copyid:
    :param pid:
    :return:
    """
    penalty = Kary(uzytkownik_id=uid, egzemplarz_id=copyid, typ_kary_id=pid)
    db.session.add(penalty)

    return commit_changes()


def insert_author(form):
    author = Autor(imie=form.name.data, nazwisko=form.surname.data)
    db.session.add(author)
    return commit_changes()


class BooksDb:

    @staticmethod
    def update_book(book, title, aid, pid, premiere_date, publ_year, ean, lang_id):
        """
        Updates information about book in database. Only admin should be allowed to make changes.
        :param book:        (obj)   : book model
        :param title:
        :param aid:         (int)   : author id
        :param pid:         (int)   : publisher id
        :param premiere_date:
        :param publ_year:   (int)   : publication year
        :param ean:
        :param lang_id:     (int)   : language id
        :return: True if commit was successful
        """

        book.tytul = title
        book.autor_id = aid
        book.wydawca_id = pid
        book.data_premiery = premiere_date
        book.rok_wydania = publ_year
        book.ean = ean
        book.jezyk_id = lang_id

        return commit_changes()

    @staticmethod
    def insert_book(title, aid, pid, premiere_date, publ_year, ean, lang_id):
        """
        Inserts book into database.
        :param title:
        :param aid:             (int)   : author id
        :param pid:             (int)   : publisher id
        :param premiere_date:
        :param publ_year:       (int)   : publication year
        :param ean:
        :param lang_id:         (int)   : language id
        :return:                (bool)  : True if transaction was successful
        """
        book = Ksiazki(tytul=title, autor_id=aid, wydawca_id=pid, data_premiery=premiere_date,
                       rok_wydania=publ_year, ean=ean, jezyk_id=lang_id)
        db.session.add(book)
        return commit_changes()

    @staticmethod
    def add_copies(form):
        """
        Add specified in form number of copies of the book specified by book id
        :param form:
        :return:
        """
        for k in range(form.count.data):
            copy = Egzemplarze(ksiazka_id=form.bid.data, biblioteka_id=form.library_id.data)
            db.session.add(copy)

        return commit_changes()

    @staticmethod
    def get_copies(bid):
        """
        Returns all copies of indicated book.
        :param bid:     (int)   : book id
        :return:        (list)  : list of copies of book
        """

        query = text(
            "SELECT * FROM v_egzemplarze WHERE ksiazka_id=:bid"
        )
        copies = db.engine.execute(query, bid=bid).fetchall()   # copies[i].atrr
        # copies = convert_to_dict_structure(copies, 'eid', 'title', 'name', 'surname', 'library_name', 'bid')

        return copies

def commit_changes():
    try:
        db.session.commit()
        return True
    except IntegrityError as e:
        print(str(e))
        db.session.rollback()
        return False


def convert_to_dict_structure(tlist, *names):
    """
    Converts list of tuples to list of dictionaries with keys passed as variable-length argument to the method.
    Number of names have to be equal length of tuples (all of tuples lengths should be also equal).
    Order of names is crucial because creation looks like: dict[name[j]] = tlist[i][j], where i = <0, len(tlist)> and
    j is equeal length of nested tuples, which have to be equeal number of passed names.
    :param tlist:   (list)  : list of tuples
    :param names:   (list)  : names have to be strings
    :return:
    """
    # if not len(tlist):
    #     print('Passed list cannot be empty')
    #     return None
    # if len(tlist[0] != len(names)):
    #     print('Length of tuple should be equal length of names')
    #     return None

    out_list = []
    for li in tlist:
        d = {}
        for k, name in enumerate(names):
            d[name] = li[k]
        out_list.append(d)

    return out_list

