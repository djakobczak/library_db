from sqlalchemy.exc import IntegrityError
from librarydb import db
from librarydb.models import Ksiazki

class DatabaseMethods:

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

        try:
            db.session.commit()
            return True
        except IntegrityError:
            db.session.rollback()
            return False

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


def commit_changes():
    try:
        db.session.commit()
        return True
    except IntegrityError as e:
        print(e)
        db.session.rollback()
        return False
