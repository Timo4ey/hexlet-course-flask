from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, email_validator
from ..users_db import Users


email_validator = email_validator.validate_email


class RegistrationForm(FlaskForm):
    nickname = StringField('Nickname',  validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])


class Validator:
    def __init__(self, data: Users) -> None:
        self.data = data
        self.errors = {}

    def validate_name(self):
        errors = {
            'len': 'Length is less then 2 or more 25 letters',
            'first_letter': 'The first letter must be in upper case'
        }
        if len(self.data.name) < 2 or len(self.data.name) > 25:
            self.errors['nickname'] = errors['len']
        elif self.data.name[0] != self.data.name[0].upper():
            self.errors['nickname'] = errors['first_letter']

    def validate_email(self):
        email = self.data.email
        try:
            email = email_validator(email)
        except ValueError as ex:
            self.errors['email'] = ex

    def is_valid(self):
        if self.errors.get('nickname') is None and\
           self.errors.get('email') is None:
            return True
        return self.errors
