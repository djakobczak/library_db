from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from librarydb.books.forms import LIBRARIES_TYPES
from librarydb.models import Uzytkownicy


class RegistrationForm(FlaskForm):
    # first argument is label in html
    name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    pin = StringField('Pesel', validators=[DataRequired(), Length(min=11, max=11, message="Pesel musi mieć długość 11 cyfr")])  # personal identity number (pesel)
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Adres', validators=[DataRequired()])
    username = StringField('Nazwa użytkownika')
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password', message="Hasła muszą się zgadzać")])
    library_id = SelectField('Biblioteka', choices=LIBRARIES_TYPES)
    submit = SubmitField('Zarejestruj się')

    def validate_pin(self, pin):
        # user = get_user(pin.data, attr='pin')
        user = Uzytkownicy.query.filter_by(pesel=pin.data).first()
        if user:
            raise ValidationError('Użytkownik o podanym peselu istnieje')

    def validate_email(self, email):
        # user = get_user(email.data, attr='email')
        user = Uzytkownicy.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Użytkownik o podanym emailu istnieje')


class UpdateAccountForm(FlaskForm):
    # first argument is label in html
    def __init__(self, user, *args, **kwargs):
        super(UpdateAccountForm, self).__init__(*args, **kwargs)
        self.user = user

    name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    pin = StringField('Pesel', validators=[DataRequired(), Length(min=11, max=11, message="Pesel musi mieć długość 11 cyfr")])  # personal identity number (pesel)
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Adres', validators=[DataRequired()])
    username = StringField('Nazwa użytkownika')
    library_id = SelectField('Biblioteka', choices=LIBRARIES_TYPES)
    submit = SubmitField('Zaktualizuj')

    def validate_pin(self, pin):
        # user = get_user(pin.data, attr='pin')
        if pin.data != self.user.pesel:
            user = Uzytkownicy.query.filter_by(pesel=pin.data).first()
            if user:
                raise ValidationError('Użytkownik o podanym peselu istnieje')

    def validate_email(self, email):
        # user = get_user(email.data, attr='email')
        if email.data != self.user.email:
            user = Uzytkownicy.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Użytkownik o podanym emailu istnieje')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Zaloguj')


class SearchUserForm(FlaskForm):
    search_value = StringField(validators=[DataRequired()], render_kw={"placeholder": "Wpisz imię bądź nazwisko"})
    submit = SubmitField('Szukaj')