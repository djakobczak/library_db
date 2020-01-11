from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional


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
    search_value = StringField(validators=[DataRequired()], render_kw={"placeholder": "Jakiej książki szukasz?"})
    submit = SubmitField('Szukaj')
