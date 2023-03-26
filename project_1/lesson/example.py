from flask import Flask, render_template, request, redirect, url_for
from .users_db.users import Users, UserMaker
from .users_db.paths import Paths


app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']


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
            'index.html',
            name=user['nickname'],
            id=user['id'],
        )
    return redirect('/users/new')


@app.route("/users")
def get_users():
    term = request.args.get('term')
    select_users = Paths.read_json()
    if term:
        select_users = list(filter(
                        lambda x: x['nickname'][:3].lower().find(term) != -1,
                        select_users))
    return render_template("users/index.html", users=select_users)


@app.route('/users/new')
def register_user():
    user_id = 0
    return render_template(
        "form/index.html",
        user_id=user_id+1)


@app.route('/users/new/<id>')
def save_user(id):
    nickname = request.args.get('nickname', '', type=str)
    email = request.args.get('email', '', type=str)
    user = Users(nickname, email)
    maker = UserMaker(user)
    maker.gen_user()
    return redirect(url_for('get_users'))
