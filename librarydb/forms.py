from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from librarydb.database import get_user


class RegistrationForm(FlaskForm):
    # first argument is label in html
    name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pin = StringField('Pesel', validators=[DataRequired(), Length(min=11, max=11, message="Pesel musi mieć długość 11 cyfr")])  # personal identity number (pesel)
    password = PasswordField('Hasło', validators=[DataRequired(), Length(min=5)])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password', message="Hasła muszą się zgadzać")])
    submit = SubmitField('Zarejestruj się')

    def validate_pin(self, pin):
        user = get_user(pin.data, attr='pin')
        if user:
            raise ValidationError('Użytkownik o podanym peselu istnieje')

    def validate_email(self, email):
        user = get_user(email.data, attr='email')
        if user:
            raise ValidationError('Użytkownik o podanym emailu istnieje')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Zaloguj')


class NewBookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    author = StringField('Autor', validators=[DataRequired()])
    category = StringField('Kategoria')
    count = IntegerField('Ilość', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Opis')
    submit = SubmitField('Potwierdź')

class SearchForm(FlaskForm):
    search_value = StringField(validators=[DataRequired()], render_kw={"placeholder": "Jakiej książki szukasz?"})
    submit = SubmitField('Szukaj')
