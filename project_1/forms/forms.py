from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired, email_validator
from ..users_db import Users
from ..users_db import Paths

email_validator = email_validator.validate_email


class RegistrationForm(FlaskForm):
    nickname = StringField('Nickname',  validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    value = HiddenField('value')


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

    @staticmethod
    def check_unique_id(id):
        db = Paths.read_json()
        new_id = list(filter(lambda x: x['id'] == id, db))
        if not new_id:
            return False
        return new_id

    @staticmethod
    def check_user_id(id):
        db = Paths.read_json()
        list_ids = list(map(lambda x: x['id'], db))
        if id in list_ids:
            return True
        return False

    @staticmethod
    def check_email(email):
        db = Paths.read_json()
        mail = list(filter(lambda x: x['email'] == email, db))
        if not mail:
            return False
        return mail
