from flask import Flask
from flask import jsonify
from flask import request

from werkzeug.exceptions import BadRequest

import db

app = Flask(__name__)


@app.route("/")
def hello():
    msg = {
        "status": "success",
        "data": "contact-api by asyks",
    }

    return jsonify(msg)


@app.route("/contact/create", methods=["POST"])
def create_contact():
    msg = {
        "status": "success",
        "data": f"contact created: {request.json}",
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
