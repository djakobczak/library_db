from librarydb import app, bcrypt, db
from flask import render_template, url_for, flash, redirect, g, request, abort
from librarydb.forms import LoginForm, RegistrationForm, NewBookForm, SearchForm
from librarydb.database import get_all_books, add_user, GOOD_ANS, get_user, insert_book, get_book,\
    update_book_db, delete_book_db
from librarydb.models import create_user, create_book, Book2
from flask_login import login_user, logout_user, current_user, login_required
# from librarydb.models import load_user

# @app.before_first_request
# def init_actions():
#     connect_db()


@app.teardown_request
def close_db(error):
    """Close connection to database."""
    if hasattr(g, 'db'):
        g.db.close()


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

# changed books to book
@app.route("/book",  methods=['GET', 'POST'])
def books():
    # cbooks = [create_book(book) for book in get_all_books()]
    page = request.args.get('page', 1, type=int)
    cbooks = Book2.query.order_by(Book2.title.asc()).paginate(page=page, per_page=5)
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search_results', search_value=form.search_value.data))

    return render_template('books.html', books=cbooks, title="książki", form=form)


@app.route("/results/<search_value>",  methods=['GET', 'POST'])
def search_results(search_value):
    """
    Route is needed, because of pagination. If we used only books route then after going to
    e.g. page 2 our search results would be deleted.
    :param search_value:
    :return:
    """
    page = request.args.get('page', 1, type=int)
    form = SearchForm()
    # search in titles and authors
    search_pattern = "%{}%".format(search_value)
    search_result = Book2.query.filter((Book2.title.like(search_pattern)) | (Book2.author.like(search_pattern))) \
        .paginate(page=page, per_page=5)

    if search_result.total == 0 and request.method == "GET":    # search failed
        flash('Brak wyników wyszukiwania', 'danger')

    if form.validate_on_submit():
        return redirect(url_for('search_results', search_value=form.search_value.data))

    return render_template('search_results.html', books=search_result, title="wyniki wyszukiwania",
                           form=form, search_value=search_value)


# need to add list of allowed method
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        ans = add_user(name=form.name.data, surname=form.surname.data,
                       pin=form.pin.data, email=form.email.data, passwd=hashed_pw)
        if ans == GOOD_ANS:
            flash(f'Konto zostało utworzone!', 'success')   # second argument - bootstrap class
            return redirect(url_for('home'))
        else:
            flash(ans, 'danger')
    return render_template('register.html', title='rejestracja', form=form) \


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = create_user(get_user(form.email.data, attr='email'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Logowanie przebiegło pomyślnie', 'success')
            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Błąd podczas logowania. Sprawdź email i hasło', 'danger')  # second argument - bootstrap class
    return render_template('login.html', title='logowanie', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Twoje konto')


@app.route("/book/<int:book_id>")
@login_required
def book_info(book_id):
    book = create_book(get_book(book_id))
    if not book:
        abort(404)
    return render_template('book_info.html', book=book)


@app.route("/account/new-book", methods=['GET', 'POST'])
@login_required
def new_book():
    if not current_user.is_admin:       # if common user tries to add book -> content forbidden
        abort(403)
    form = NewBookForm()
    if form.validate_on_submit():
        ans = insert_book(title=form.title.data, author=form.author.data, category=form.category.data,
                    count=form.count.data, description=form.description.data)
        if ans == GOOD_ANS:
            flash('Książka została dodana do bazy', 'success')
            return redirect(url_for('new_book'))        # flush fields, simple but slow
        else:
            flash(ans, 'danger')
    return render_template('new_book.html', form=form, legend='Dodaj nową książkę')


@app.route("/book/<int:book_id>/update", methods=['GET', 'POST'])
@login_required
def update_book(book_id):
    if not current_user.is_admin:
        abort(403)
    book = create_book(get_book(book_id))
    form = NewBookForm()
    if form.validate_on_submit():
        ans = update_book_db(book_id=book_id, title=form.title.data, author=form.author.data, category=form.category.data,
                             count=form.count.data, description=form.description.data)
        if ans == GOOD_ANS:
            flash('Książka została zaktualizowana', 'success')
            return redirect(url_for('book_info', book_id=book.bid))
        else:
            flash(ans, 'danger')
            return redirect(url_for('update_book', book_id=book.bid))
    else:
        form.title.data = book.title
        form.author.data = book.author
        form.category.data = book.category
        form.count.data = book.count
        form.description.data = book.description
    return render_template('new_book.html', form=form, legend='Zaktualizuj informacje')


@app.route("/book/<int:book_id>/delete", methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        abort(403)
    book = create_book(get_book(book_id))
    ans = delete_book_db(book.bid)
    if ans == GOOD_ANS:
        flash('Książka została usunięta z bazy', 'success')
        return redirect(url_for('books'))
    else:
        flash(ans, 'danger')
        return redirect(url_for('book_info', book_id=book_id))

