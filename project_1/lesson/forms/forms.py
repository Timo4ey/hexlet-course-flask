from flask_wtf import FlaskForm
from wtforms import StringField
# from wtforms.validators import Email,


class RegistrationForm(FlaskForm):
    nickname = StringField('Nickname')  # , validators=[DataRequired()]
    email = StringField('Email')
