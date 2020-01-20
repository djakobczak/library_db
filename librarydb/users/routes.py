from flask import Blueprint, request, redirect, url_for, render_template, flash, abort
from flask_login import login_required, current_user, login_user, logout_user

from librarydb import app, db, bcrypt
from librarydb.books.forms import PenaltyForm, SearchForm
from librarydb.books.utils import add_penalty, BooksDb
from librarydb.models import Uzytkownicy, TypKonta, Rezerwacje, Ksiazki
from librarydb.settings import *
from librarydb.users.forms import LoginForm, RegistrationForm, SearchUserForm, UpdateAccountForm
from librarydb.users.utils import reserved_books_by_user_alchemy, user_borrowed_books, update_user_information, \
    get_penalties, cancel_penalty_db, pay_penalty_db, get_payments, return_book_db

users = Blueprint('users', __name__)


# need to add list of allowed method
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # noinspection PyArgumentList
        user = Uzytkownicy(imie=form.name.data, nazwisko=form.surname.data,
                           pesel=form.pin.data, email=form.email.data,
                           adres=form.address.data, nazwa_uzytkownika=form.username.data,
                           haslo=hashed_password, typ_konta=TypKonta.query.filter_by(id=1).first())  # 2 means user
        db.session.add(user)
        db.session.commit()
        # ans = add_user(name=form.name.data, surname=form.surname.data,
        #                pin=form.pin.data, email=form.email.data, passwd=hashed_pw) # old version, based on sql quaries
        flash(f'Konto zostało utworzone!', 'success')  # second argument - bootstrap class
        return redirect(url_for('users.login'))
        # else:
        #   flash(ans, 'danger')
    return render_template('register.html', title='rejestracja', form=form, ADMIN_ID=ADMIN_ID)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = Uzytkownicy.query.filter_by(email=form.email.data).first()
        # user = create_user(get_user(form.email.data, attr='email'))
        if user and bcrypt.check_password_hash(user.haslo, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logowanie przebiegło pomyślnie', 'success')
            app.logger.info('%s logged in successfully', user)
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Błąd podczas logowania. Sprawdź email i hasło', 'danger')  # second argument - bootstrap class
    return render_template('login.html', title='logowanie', form=form)


@users.route("/logout")
def logout():
    logout_user()
    app.logger.info('%s logged out successfully', current_user)
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    # rbooks = reserved_books_by_user(db, current_user.id)  # !TODO try to change to dict by using ORM
    rbooks = reserved_books_by_user_alchemy(db, current_user.id)
    bbooks = user_borrowed_books(current_user.id)
    penalties = get_penalties(db, current_user.id)

    return render_template('account.html', title='Twoje konto', rbooks=rbooks, bbooks=bbooks,
                           penalties=penalties, ADMIN_ID=ADMIN_ID)


@users.route("/account/users", methods=['GET', 'POST'])
@login_required
def users_list():
    if current_user.typ_konta_id != ADMIN_ID:  # if common user tries to add book -> content forbidden
        abort(403)
    page = request.args.get('page', 1, type=int)
    users = Uzytkownicy.query.order_by(Uzytkownicy.nazwisko.asc()).paginate(page=page, per_page=10)

    form = SearchUserForm()
    if form.validate_on_submit():
        pass  # !TODO
        # return redirect(url_for('books.search_results', search_value=form.search_value.data))

    return render_template('users_list.html', title='Czytelnicy', users=users, form=form)


@users.route("/account/users/<int:uid>", methods=['GET', 'POST'])
@login_required
def user_info(uid):  # all users should have access to this route?
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)
    user = Uzytkownicy.query.get_or_404(int(uid))

    search_form = SearchForm()
    rbooks = reserved_books_by_user_alchemy(db, user.id)
    bbooks = user_borrowed_books(user.id)
    penalties = get_penalties(db, user.id)
    payments = get_payments(db, user.id)
    return render_template('user_info.html', user=user, rbooks=rbooks, bbooks=bbooks,
                           penalties=penalties, payments=payments, search_form=search_form)


@users.route("/account/users/<int:uid>/update", methods=['GET', 'POST'])
@login_required
def update_account(uid):  # all users should have access to this route?
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    user = Uzytkownicy.query.get_or_404(uid)
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)
    # book = create_book(get_book(book_id))
    form = UpdateAccountForm(user)
    if form.validate_on_submit():
        ans = update_user_information(db, user, form)
        if ans:
            flash('Informacje zostały zaktualizowane', 'success')
        else:
            flash('Operacja się nie powiadła, sprawdź czy na pewno podane identyfikatory istnieją w bazie danych',
                  'danger')
        return redirect(url_for('users.user_info', uid=user.id))
    else:
        form.name.data = user.imie
        form.surname.data = user.nazwisko
        form.pin.data = user.pesel
        form.email.data = user.email
        form.address.data = user.adres
        form.username.data = user.nazwa_uzytkownika

    return render_template('register.html', form=form, legend='Zaktualizuj informacje', ADMIN_ID=ADMIN_ID)


@users.route("/account/users/<int:uid>/penalty", methods=['GET', 'POST'])
@login_required
def penalize_user(uid):
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    form = PenaltyForm()
    if form.validate_on_submit():
        if add_penalty(db, uid=uid, copyid=form.copyid.data, pid=form.penalty_type.data):
            flash(f'Użytkownik o id {uid} dostał karę', 'success')

            return redirect(url_for('users.user_info', uid=uid))
        else:
            flash('Dodanie kary się nie powiodło, sprawdź czy podane ID egzemplarza istnieje w bazie', 'danger')

    return render_template('penalize.html', ADMIN_ID=ADMIN_ID, form=form)


@users.route("/account/users/<int:uid>/penalty/<int:pid>/remove", methods=['POST'])
@login_required
def cancel_penalty(uid, pid):
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    cancel_penalty_db(db, uid=uid, pid=pid)
    flash('Kara została wycofana', 'success')

    return redirect(url_for('users.user_info', uid=uid))


@users.route("/account/users/<int:uid>/penalty/<int:pid>/pay", methods=['POST'])
@login_required
def pay_penalty(uid, pid):
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    pay_penalty_db(db, pid)
    app.logger.info(f'Penalty was paid, uid={uid}, penalty_id={pid}')
    flash('Oplacono kare', 'success')
    return redirect(url_for('users.user_info', uid=uid))


@users.route("/account/users/<int:uid>/return/<int:lend_id>", methods=['POST'])
@login_required
def return_book(uid, lend_id):
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)

    if return_book_db(lend_id):
        flash('Ksiązkę oddano', 'success')
    else:
        flash('Błąd podczas oddawnia ksążki', 'danger')
    return redirect(url_for('users.user_info', uid=uid))


@users.route("/account/users/<int:uid>/borrow/<int:bid>/<int:cid>", methods=['POST'])
@login_required
def borrow_book(uid, cid, bid):
    """

    :param bid:
    :param uid:
    :param cid:     (int)   : copy id
    :return:
    """
    if current_user.typ_konta_id != ADMIN_ID:
        abort(403)
    if BooksDb.borrow_book(cid=cid, bid=bid, uid=uid):
        flash('Książka została wypożyczona', 'success')
    else:
        flash('Błąd podczas wypożyczenia, pradopodobnie książka została zarezerwowana', 'danger')

    return redirect(url_for('users.user_info', uid=uid))