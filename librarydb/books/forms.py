from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Optional

from librarydb.books.utils import get_penalties_tuples, \
    get_libraries_tuples

# values have to be strings, if integers -> Not a Valid Choice Error
PENALITIES_TYPES = get_penalties_tuples()
LIBRARIES_TYPES = get_libraries_tuples()


class NewBookForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired()])
    # author = StringField('Autor', validators=[DataRequired()])
    aid = IntegerField('ID autora', validators=[DataRequired(), NumberRange(min=0)])
    pid = IntegerField('ID wydawcy', validators=[DataRequired(), NumberRange(min=0)])
    premiere_date = DateField('Data premiery', format='%m/%d/%Y', validators=[Optional()])
    publication_date = IntegerField('Rok wydania', validators=[Optional()])
    ean = StringField('Ean')
    lang_id = IntegerField('ID języka', validators=[DataRequired()])
    submit = SubmitField('Potwierdź')

class SearchForm(FlaskForm):
    search_value = StringField('', validators=[DataRequired()], render_kw={"placeholder": "Jakiej książki szukasz?"})
    submit = SubmitField('Szukaj')


class PenaltyForm(FlaskForm):
    copyid = IntegerField('ID egzemplarza', validators=[DataRequired()])
    penalty_type = SelectField('Typ kary', choices=PENALITIES_TYPES)
    submit = SubmitField('Dodaj')


class NewAuthorForm(FlaskForm):
    name = StringField('Imię', validators=[DataRequired()])
    surname = StringField('Nazwisko')
    submit = SubmitField('Dodaj')

class AddCopiesForm(FlaskForm):
    bid = StringField('ID książki', validators=[DataRequired()])
    library_id = SelectField('Biblioteka', choices=LIBRARIES_TYPES)
    count = IntegerField('Ilość', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Dodaj')

class AddOpinionForm(FlaskForm):
    content = TextAreaField('Opinia', validators=[DataRequired()])
    submit = SubmitField('Dodaj opinie')