from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy import text
from datetime import datetime

from librarydb import app, db
from librarydb.books.forms import SearchForm, NewBookForm, NewAuthorForm, AddCopiesForm, AddOpinionForm
from librarydb.books.utils import available_books, insert_author, BooksDb
from librarydb.models import Ksiazki, Egzemplarze, Rezerwacje, Wypozyczenia, Opinie
from librarydb.settings import *

books = Blueprint('books', __name__)


# changed books to book
@books.route("/book", methods=['GET', 'POST'])
@books.route("/book/<int:uid>", methods=['GET', 'POST'])
def books_list(uid=None):
    page = request.args.get('page', 1, type=int)
    # cbooks = Book2.query.order_by(Book2.title.asc()).paginate(page=page, per_page=5)
    cbooks = Ksiazki.query.order_by(Ksiazki.tytul.asc()).paginate(page=page, per_page=5)

    form = SearchForm()
    if form.validate_on_submit():
        if uid:
            return redirect(url_for('books.search_results', search_value=form.search_value.data, uid=uid))
        else:
            return redirect(url_for('books.search_results', search_value=form.search_value.data))

    return render_template('books.html', books=cbooks, title="książki", form=form, uid=uid)


@books.route("/results/<search_value>", methods=['GET', 'POST'])
@books.route("/results/<search_value>/<int:uid>", methods=['GET', 'POST'])
def search_results(search_value, uid=None):
    """
    Route is needed, because of pagination. If we used only books route then after going to
    e.g. page 2 our search results would be deleted.
    :param uid:
    :param search_value:
    :return:
    """
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    # search in titles and authors
    search_pattern = "%{}%".format(search_value)
    search_result = Ksiazki.query.filter((Ksiazki.tytul.like(search_pattern))) \
        .paginate(page=page, per_page=5)  # | (Ksiazki.autor.like(search_pattern))

    if search_result.total == 0 and request.method == "GET":  # search failed
        flash('Brak wyników wyszukiwania', 'danger')

    if form.validate_on_submit():
        if uid:
            return redirect(url_for('books.search_results', search_value=form.search_value.data, uid=uid))
        else:
            return redirect(url_for('books.search_results', search_value=form.search_value.data))

    return render_template('search_results.html', books=search_result, title="wyniki wyszukiwania",
                           form=form, search_value=search_value, uid=uid)


@books.route("/book-info/<int:book_id>")
@books.route("/book-info/<int:book_id>/<int:uid>")
@login_required
def book_info(book_id, uid=None):
    # book = create_book(get_book(book_id))
    book = Ksiazki.query.get(int(book_id))
    if not book:
        abort(404)

    abooks = available_books(db, book_id)
    copies = BooksDb.get_copies(book_id)
    categories = BooksDb.get_categories(book_id)
    opinions = Opinie.query.filter(Opinie.ksiazka_id == book_id).all()

    return render_template('book_info.html', book=book, book_count=abooks, copies=copies,
                           categories=categories, uid=uid, opinions=opinions,
                           ADMIN_ID=ADMIN_ID, USER_ID=USER_ID)


@books.route("/book-info/<int:book_id>/opinion", methods=['GET', 'POST'])
@login_required
def add_opinion(book_id):
    form = AddOpinionForm()
    if form.validate_on_submit():
        opinion = Opinie(ksiazka_id=book_id, uzytkownik_id=current_user.id,
                         opinia=form.content.data, data_dodania=datetime.now())
        db.session.add(opinion)
        try:
            db.session.commit()
            flash('Twoja opinia została dodana', 'success')
            return redirect(url_for('books.book_info', book_id=book_id))
        except IntegrityError:
            db.session.rollback()
            flash('Wystąpił błąd, spórbuj ponownie później', 'danger')
            return redirect(url_for('books.book_info', book_id=book_id))

    return render_template('add_opinion.html', form=form, legend='Dodaj swoją opinię')


@books.route("/<int:book_id>/opinion/<int:opinion_id>/update", methods=['GET', 'POST'])
@login_required
def update_opinion(opinion_id, book_id):
    opinion = Opinie.query.get_or_404(opinion_id)
    if opinion.uzytkownik != current_user and current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    form = AddOpinionForm()
    if form.validate_on_submit():
        opinion.opinia = form.content.data
        opinion.data_dodania = datetime.now()
        db.session.commit()
        flash('Opinia została zaktualizowana', 'success')
        return redirect(url_for('books.book_info', book_id=book_id))
    elif request.method == 'GET':
        form.content.data = opinion.opinia

    return render_template('add_opinion.html', form=form, legend='Zaktualizuj swoją opinię')

@books.route("/<int:book_id>/opinion/<int:opinion_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_opinion(opinion_id, book_id):
    opinion = Opinie.query.get_or_404(opinion_id)
    if opinion.uzytkownik != current_user and current_user.typ_konta_id != ADMIN_ID:
        abort(403)
    db.session.delete(opinion)
    db.session.commit()
    flash('Opinia została usunięta', 'success')
    return redirect(url_for('books.book_info', book_id=book_id))


@books.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    book = Ksiazki.query.get_or_404(book_id)
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)
    # book = create_book(get_book(book_id))
    form = NewBookForm()
    if form.validate_on_submit():
        # old
        # ans = update_book_db(book_id=book_id, title=form.title.data, author=form.author.data,
        #                      category=form.category.data,
        #                      count=form.count.data, description=form.description.data)
        ans = BooksDb.update_book(book=book, title=form.title.data, aid=form.aid.data,
                                  pid=form.pid.data, premiere_date=form.premiere_date.data,
                                  publ_year=form.publication_date.data, ean=form.ean.data,
                                  lang_id=form.lang_id.data)
        if ans:
            flash('Książka została zaktualizowana', 'success')
            return redirect(url_for('books.book_info', book_id=book.id))
        else:
            flash('Operacja się nie powiadła, sprawdź czy na pewno podane identyfikatory istnieją w bazie danych',
                  'danger')
            return redirect(url_for('books.update_book', book_id=book.id))
    else:
        form.title.data = book.tytul
        form.aid.data = book.autor.id
        form.pid.data = book.wydawca.id
        form.ean.data = book.ean
        form.premiere_date.data = book.data_premiery
        form.publication_date.data = book.rok_wydania
        form.lang_id.data = book.jezyk.id
    return render_template('new_book.html', form=form, legend='Zaktualizuj informacje')


@books.route("/book/<int:book_id>/delete", methods=['POST'])
@login_required
def delete_book(book_id):
    book = Ksiazki.query.get_or_404(book_id)
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)
    db.session.delete(book)
    try:
        db.session.commit()
        flash('Książka została usunięta z bazy', 'success')
        app.logger.info('%s deleted sucessfully', book)  # should be id
        return redirect(url_for('books.books_list'))
    except IntegrityError as e:
        flash('Operacja się nie powiodła, spróbuj jeszcze raz', 'danger')
        return redirect(url_for('books.book_info', book_id=book_id))
    # ans = delete_book_db(book.id)
    # if ans == GOOD_ANS:
    #     flash('Książka została usunięta z bazy', 'success')
    #     return redirect(url_for('books'))
    # else:
    #     flash(ans, 'danger')
    #     return redirect(url_for('book_info', book_id=book_id))


@books.route("/account/new-book", methods=['GET', 'POST'])
@login_required
def new_book():
    if current_user.typ_konta_id != ADMIN_ID:  # if common user tries to add book -> content forbidden
        abort(403)
    form = NewBookForm()
    if form.validate_on_submit():
        # ans = insert_book(title=form.title.data, author=form.author.data, category=form.category.data,
        #                   count=form.count.data, description=form.description.data)
        ans = BooksDb.insert_book(title=form.title.data, aid=form.aid.data,
                                  pid=form.pid.data, premiere_date=form.premiere_date.data,
                                  publ_year=form.publication_date.data, ean=form.ean.data,
                                  lang_id=form.lang_id.data)
        if ans:
            flash('Książka została dodana do bazy', 'success')
            app.logger.info('New book with title %s added sucessfully', form.title.data)  # should be id
            return redirect(url_for('books.new_book'))  # flush fields, simple but slow
        else:
            flash(ROLLBACK_MSG, 'danger')
    return render_template('new_book.html', form=form, legend='Dodaj nową książkę do bazy')


@books.route("/account/new-author", methods=['GET', 'POST'])
@login_required
def new_author():
    if current_user.typ_konta_id != ADMIN_ID:  # if common user tries to add book -> content forbidden
        abort(403)
    form = NewAuthorForm()
    if form.validate_on_submit():
        ans = insert_author(form)
        if ans:
            flash('Autor została dodana do bazy', 'success')
            return redirect(url_for('books.new_author'))  # flush fields, simple but slow
        else:
            flash(ROLLBACK_MSG, 'danger')
    return render_template('new_author.html', form=form, legend='Dodaj nowego autora do bazy')


@books.route("/book/reserve/<int:book_id>", methods=['POST'])
@login_required
def reserve(book_id):
    # TODO check whether user can borrow a book, - transaction
    is_reserved = Rezerwacje.query. \
        filter(Rezerwacje.uzytkownik_id == current_user.id, Rezerwacje.ksiazka_id == book_id).first()
    if is_reserved:
        flash('Nie możesz zarezerwować dwa razy tej samej książki', 'danger')
        return redirect(url_for('books.book_info', book_id=book_id))

    reservation = Rezerwacje(uzytkownik_id=current_user.id, data_rezerwacji=datetime.now(), ksiazka_id=book_id)
    abooks = available_books(db, book_id)
    db.session.add(reservation)  #
    if abooks < 1:
        db.session.rollback()
        flash('Rezerwacja się nie powiodła, egzemplarze się skończyły', 'danger')
        app.logger.error('Reservation is not possible, no of copies=%s ,book_id=%s, user_id=%s', abooks, book_id,
                         current_user.id)
        return redirect(url_for('books.book_info', book_id=book_id))

    try:
        db.session.commit()
        flash('Rezerwacja się powiodła', 'success')
        return redirect(url_for('books.book_info', book_id=book_id))

    except IntegrityError as e:
        app.logger.error('Reservation aborted, book_id=%s, user_id=%s', book_id, current_user.id)
        flash('Rezerwacja się nie powiodła', 'danger')
        return redirect(url_for('books.book_info', book_id=book_id))


@books.route("/book/reserve/<int:bcid>/remove/<int:uid>", methods=['POST'])
@login_required
def remove_reservation(bcid, uid):  # bcid = book copy id
    res = Rezerwacje.query.filter_by(ksiazka_id=bcid, uzytkownik_id=uid).first()
    db.session.delete(res)
    db.session.commit()
    flash('Odwołano rezerwacje', 'danger')
    if current_user.id == uid:
        return redirect(url_for('users.account'))
    else:
        return redirect(url_for('users.user_info', uid=uid))


@books.route("/account/add-copies", methods=['GET', 'POST'])
@login_required
def add_copies():
    if current_user.typ_konta_id != ADMIN_ID:  # if common user tries to add book -> content forbidden
        abort(403)
    form = AddCopiesForm()
    if form.validate_on_submit():
        ans = BooksDb.add_copies(form)

        if ans:
            flash('Egzemplarze zostały dodane do bazy', 'success')
            app.logger.info('Coppies of book with id % added', form.bid.data)  # should be id
            return redirect(url_for('books.add_copies'))  # flush fields, simple but slow
        else:
            flash(ROLLBACK_MSG, 'danger')
    return render_template('add_copies.html', form=form, legend='Dodaj egzemplarze do bazy')
