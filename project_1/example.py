import json
from flask import (Flask, render_template,
                   request, redirect, url_for,
                   flash, get_flashed_messages,
                   make_response, session)
from .users_db.users import Users, UserMaker
from .users_db.paths import Paths
from .forms.forms import RegistrationForm, Validator
from flask_session import Session
from .config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)
Session(app)


@app.route('/', methods=["GET", "POST"])
def main_page():
    return redirect(url_for('get_users'))


@app.route('/users/<int:id>', methods=["GET"])
def get_name(id):
    data = Paths.read_json()
    result = tuple(filter(lambda x: x.get('id') == id, data))
    message = get_flashed_messages(with_categories=True)
    if len(result) == 0:
        user = ''
    else:
        (user, ) = result
    if user:
        return render_template("index.html", id=user['id'],
                               name=user['nickname'],
                               email=user['email'],
                               messages=message)
    return redirect(url_for("register_user"))


@app.route("/users", methods=['GET'])
def get_users():
    term = request.args.get('term')
    select_user = Paths.read_json()
    messages = get_flashed_messages(with_categories=True)
    if term:
        select_user = list(filter(
                        lambda x: x['nickname'][:3].lower().find(term) != -1,
                        select_user
                        ))

    users_registered = json.loads(request.cookies.get('name', json.dumps([])))
    return render_template("users/index.html",
                           users=select_user,
                           messages=messages,
                           users_registered=users_registered,
                           session=session)


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
    validator = Validator(user)
    maker = UserMaker(user)
    ids = list(map(lambda x: x['id'], maker.read_json_file()))
    new_id = validator.check_unique_id(user.get_id)
    if new_id:
        new_id = max(ids)
        user.get_id = new_id + 1

    validator.validate_name()
    validator.validate_email()
    if validator.is_valid() is True:
        flash("User was added successfully", "success")
        maker.gen_user()
        reg_user = json.loads(request.cookies.get('name', json.dumps([])))
        reg_user.append(maker.data.output())

        resp = make_response(redirect(url_for('get_users'), 302))
        cookie = json.dumps(reg_user)
        resp.set_cookie('name', cookie)
        return resp
    return render_template(
        "form/index.html",
        form=form,
        errors=validator.is_valid()
        ), 422


@app.route("/users/<int:id>/edit")
def edit_user_page(id):
    form = RegistrationForm()
    ids = Validator.check_user_id(id)
    data = Validator.check_unique_id(id)
    if ids:
        return render_template("form/edit_user.html",
                               form=form,
                               errors={},
                               id=id,
                               data=data[0])
    if not ids:
        return render_template('errors/422.html')


@app.route('/users/<int:id>/edit', methods=["POST"])
def edit_user(id):
    data = request.form.to_dict()
    instance = Users(data['nickname'], data['email'])
    user = UserMaker(instance)
    user.edit_users(id)
    flash("User has been updated", 'success')
    return redirect(url_for('get_name', id=id))


@app.get("/users/<int:id>/confirm")
def confirm_delete(id):
    return render_template('form/confirmed.html', id=id)


@app.post("/users/<int:id>/delete")
def delete_user(id):
    user = UserMaker(Users())
    data = user.read_json_file()
    temp_id = 0
    for indx in range(len(data)):
        if data[indx]['id'] == id:
            temp_id = indx
    del data[temp_id]
    user.write_into_json(data)
    flash('User has been deleted', 'success')
    return redirect(url_for('get_users'))


@app.get('/login')
def login_page():
    form = RegistrationForm()
    return render_template('users/login.html',
                           form=form, errors={},
                           session=session)


@app.post('/login')
def login():
    form = RegistrationForm()
    email = form.email.data
    validator = Validator.check_email(email)
    if validator:
        if session.get('email', None) is None:
            session['email'] = email
        else:
            session['email'] = email
        flash('You are IN', 'success')
        return redirect(url_for('get_users'))
    return render_template('users/login.html',
                           form=form,
                           errors=validator,
                           session=session), 422
