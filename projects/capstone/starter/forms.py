from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL


class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = StringField(
        'gender', validators=[DataRequired()]
    )


class ProjectForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    release_date = DateTimeField(
        'release_date', validators=[DataRequired()]
    )
