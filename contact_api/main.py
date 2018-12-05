from flask import Flask
from flask import jsonify
from flask import request
from flask import g

from werkzeug.exceptions import BadRequest
import sqlite3


app = Flask(__name__)

app.config.update({
    "DATABASE": "file::memory:?cache=shared",
    "DEBUG": True,
    "SECRET_KEY": 'devkey',
    "USERNAME": 'admin',
    "PASSWORD": 'default',
})


def connect_db():
    return_val = sqlite3.connect(app.config['DATABASE'])
    return_val.row_factory = sqlite3.Row

    return return_val


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db


@app.before_first_request
def init_db():
    db = get_db()
    db.cursor().executescript(
        """CREATE TABLE contacts (
            id integer primary key autoincrement,
            email text,
            name text
        );"""
    )
    insert_one_contact('ba@ba', 'crab')  # REMOVE! just test seeding the db
    print('Initialized the database.')


def insert_one_contact(email, name):
    db = get_db()
    db.execute(
        "INSERT INTO contacts (email, name) VALUES (?, ?);",
        (email, name,),
    )


@app.route("/")
def hello():
    msg = {
        "status": "success",
        "data": "contact-api by asyks",
    }

    return jsonify(msg)


@app.route("/contact/create", methods=["POST"])
def create_contact():
    insert_one_contact(request.json['email'], request.json['name'])
    db = get_db()
    cur = db.execute('SELECT * FROM contacts;')
    total = len(cur.fetchall())

    msg = {
        "status": "success",
        "data": f"contact created: {request.json}, total: {total}",
    }

    return jsonify(msg)


@app.errorhandler(BadRequest)
def handle_bad_request(exception):
    err_msg = {
        "status": "error",
        "message": (
            f"{exception.name}: JSON could not be "
            "decoded from request body"
        )
    }
    response = jsonify(err_msg)
    response.status_code = exception.code

    return response
