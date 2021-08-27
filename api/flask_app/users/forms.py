from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField, TextField
from wtforms.validators import ValidationError, DataRequired, Length


class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        pass


class TestForm(FlaskForm):
    first_name = TextField("First Name", validators=[DataRequired()])
    middle_name = TextField("Middle Name")
    last_name = TextField("Last Name", validators=[DataRequired()])