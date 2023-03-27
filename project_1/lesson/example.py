from flask import (Flask, render_template,
                   request, redirect, url_for,
                   flash, get_flashed_messages)
from .users_db.users import Users, UserMaker
from .users_db.paths import Paths
import os
from .forms.forms import RegistrationForm, Validator


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
def main_page():
    id = request.args.get('id')
    nickname = request.args.get('nickname')
    return render_template("index.html", id=id, nickname=nickname)


@app.route('/users/<int:id>', methods=["GET"])
def get_name(id):
    data = Paths.read_json()
    result = tuple(filter(lambda x: x.get('id') == id, data))
    if len(result) == 0:
        user = ''
    else:
        (user, ) = result
    if user:
        return render_template("index.html", id=user['id'],
                               name=user['nickname'])
    return redirect(url_for("register_user"))


@app.route("/users", methods=['GET'])
def get_users():
    term = request.args.get('term')
    select_user = Paths.read_json()
    messages = get_flashed_messages(with_categories=True)
    if term:
        select_user = list(filter(
                        lambda x: x['nickname'][:3].lower().find(term) != -1,
                        select_user))
    return render_template("users/index.html",
                           users=select_user, messages=messages)


@app.route('/users/new', methods=["GET"])
def register_user():
    form = RegistrationForm()
    return render_template(
        "form/index.html",
        form=form,
        errors={})


@app.route('/users', methods=["POST"])
def save_user():
    form = RegistrationForm()
    nickname = form.nickname.data
    email = form.email.data

    user = Users(nickname, email)

    # !!! Need to add as a new method in Validator
    db = Paths.read_json()
    new_id = list(filter(lambda x: x['id'] == user.id, db))
    if new_id:
        new_id = max(db, key=lambda x: x.get('id'))
        user.get_id = new_id['id'] + 1

    validator = Validator(user)
    validator.validate_name()
    validator.validate_email()
    if validator.is_valid() is True:
        flash("User was added successfully", "success")
        maker = UserMaker(user)
        maker.gen_user()
        return redirect(url_for('get_users'), 302)
    return render_template(
        "form/index.html",
        form=form,
        errors=validator.is_valid())
