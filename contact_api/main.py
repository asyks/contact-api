from flask import Flask

import db

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
