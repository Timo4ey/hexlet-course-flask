from flask import Flask


app = Flask(__name__)


@app.get('/users')
def users_get():
    return "GET /users"


@app.post('/users')
def users_post():
    return "Users", 302


@app.route("/course/<int:id>")
def get_course(id):
    return f"Course id: {id}"
