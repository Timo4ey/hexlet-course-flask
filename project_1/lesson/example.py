from flask import Flask, render_template, request, redirect, url_for
from .users_db.users import Users, UserMaker
from .users_db.paths import Paths
import os
from .forms.forms import RegistrationForm, Validator


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template("index.html")


@app.route('/users/<int:id>')
def get_name(id):
    data = Paths.read_json()
    result = tuple(filter(lambda x: x.get('id') == id, data))
    if len(result) == 0:
        user = ''
    else:
        (user, ) = result
    if user:
        return render_template(
            url_for('main_page'),
            name=user['nickname'],
            id=user['id'],
        )
    return redirect(url_for("register_user"))


@app.route("/users")
def get_users():
    term = request.args.get('term')
    select_users = Paths.read_json()
    if term:
        select_users = list(filter(
                        lambda x: x['nickname'][:3].lower().find(term) != -1,
                        select_users))
    return render_template("users/index.html", users=select_users)


@app.route('/users/new', methods=["GET"])
def register_user():
    form = RegistrationForm()
    return render_template(
        "form/index.html",
        form=form,
        errors={})


@app.route('/users', methods=["POST", "GET"])
def save_user():
    form = RegistrationForm()
    nickname = form.nickname.data
    email = form.email.data

    user = Users(nickname, email)
    validator = Validator(user)
    validator.validate_name()
    validator.validate_email()
    if validator.is_valid() is True:
        maker = UserMaker(user)
        maker.gen_user()
        return redirect(url_for('get_users'), 302)
    return render_template(
        "form/index.html",
        form=form,
        errors=validator.is_valid())
