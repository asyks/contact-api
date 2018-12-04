from flask import Flask
from flask import g

import sqlite3

app = Flask(__name__)

DATABASE = ":memory:"


def get_db_conn():
    conn = getattr(g, '_dbconnection', None)
    if conn is None:
        conn = g._database = sqlite3.connect(DATABASE)
    return conn


@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_dbconnection', None)
    if conn is not None:
        conn.close()


def init_db():
    with app.app_context():
        db = get_db_conn()
        db.cursor().executescript(
            """CREATE TABLE contacts (
                first_name text,
                last_name text,
                email text,
                phone integer,
                address text
            )"""
        )
        db.commit()
