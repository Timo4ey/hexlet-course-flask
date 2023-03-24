from flask import Flask, render_template, request


app = Flask(__name__)

users = ['mike', 'mishel', 'adel', 'keks', 'kamila']

# @app.get('/users')
# def users_get():
#     return "GET /users"


# @app.post('/users')
# def users_post():
#     return "Users", 302


@app.route("/course/<int:id>")
def get_course(id):
    return f"Course id: {id}"


@app.route('/users/<id>')
def get_name(id):
    return render_template(
        'index.html',
        name=id,
    )


@app.route("/users")
def get_users():
    term = request.args.get('term')
    select_users = users
    print(term)
    if term:
        select_users = list(filter(lambda x: x.find(term) != -1, select_users))
    return render_template("users/index.html", users=select_users)
