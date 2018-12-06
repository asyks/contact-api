from functools import wraps
import os

from flask import Flask
from flask import jsonify
from flask import request

from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import MethodNotAllowed
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)

app.config.update({
    "SQLALCHEMY_DATABASE_URI": "sqlite://",
    "SQLALCHEMY_TRACK_MODIFICATIONS": True,
    "DEBUG": True,
})

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, default=True, nullable=False)
    name = db.Column(db.String(80), nullable=True)
    company = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=False)
    updated_by = db.Column(db.String(120), nullable=False)

    @property
    def data_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "updated_by": self.updated_by,
        }

    @classmethod
    def get_single(cls, **kwargs):
        inst = cls.query.filter_by(active=True, **kwargs).first()
        if not inst:
            raise InternalServerError(
                "Contact does not exist, or has been deleted"
            )

        return inst


db.create_all()


def success_resp_msg(data):
    return {
        "status": "success", "data": data
    }


def error_resp_msg(msg):
    return {
        "status": "error", "message": msg
    }


def check_auth(username, password):
    return (
        username == os.environ["USERNAME"] and
        password == os.environ["PASSWORD"]
    )


def requires_auth(view):
    @wraps(view)
    def auth_wrapper(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            raise Unauthorized
        return view(*args, **kwargs)

    return auth_wrapper


@app.route("/")
def hello():
    msg = success_resp_msg("contact-api by asyks")

    return jsonify(msg)


@app.route("/contact", methods=["GET"])
def get_one_contact():
    if "id" not in request.json:
        raise InternalServerError("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json["id"])
    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contact/create", methods=["POST"])
@requires_auth
def create_contact():
    if "email" not in request.json:
        raise InternalServerError(
            "Field 'email' is required but was not found in request body"
        )

    contact = Contact(
        name=request.json.get("name"),
        company=request.json.get("company"),
        email=request.json["email"],
        updated_by=request.authorization.username,
    )
    db.session.add(contact)
    db.session.commit()

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contact/update", methods=["PUT"])
@requires_auth
def update_contact():
    if "id" not in request.json:
        raise InternalServerError("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json["id"])
    contact.updated_by = request.authorization.username
    if "name" in request.json:
        contact.name = request.json["name"]
    if "company" in request.json:
        contact.company = request.json["company"]
    if "email" in request.json:
        contact.email = request.json["email"]

    db.session.commit()

    msg = success_resp_msg(contact.data_dict)
    response = jsonify(msg)
    response.status_code = 201

    return response


@app.route("/contact/delete", methods=["DELETE"])
@requires_auth
def delete_contact():
    if "id" not in request.json:
        raise InternalServerError("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json["id"])
    contact.updated_by = request.authorization.username
    contact.active = False
    db.session.commit()

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contacts", methods=["GET"])
def get_contacts():
    if request.json:
        if "active" in request.json:
            raise InternalServerError(
                "Field 'active' is not supported for querying"
            )

        contacts = Contact.query.filter_by(active=True, **request.json).all()
    else:
        contacts = Contact.query.all()

    msg = success_resp_msg([contact.data_dict for contact in contacts])

    return jsonify(msg)


@app.errorhandler(BadRequest)
def handle_bad_request(exception):
    err_msg = error_resp_msg(
        f"{exception.name}: JSON could not be decoded from request body"
    )
    response = jsonify(err_msg)
    response.status_code = exception.code

    return response


@app.errorhandler(Unauthorized)
@app.errorhandler(InternalServerError)
@app.errorhandler(MethodNotAllowed)
def handle_error(exception):
    err_msg = error_resp_msg(
        f"{exception.name}: {exception.description}"
    )
    response = jsonify(err_msg)
    response.status_code = exception.code

    return response
