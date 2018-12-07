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
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    company = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    home_phone = db.Column(db.Integer, nullable=True)
    mobile_phone = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(280), nullable=True)
    address_2 = db.Column(db.String(280), nullable=True)
    updated_by = db.Column(db.String(120), nullable=False)

    @property
    def data_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "email": self.email,
            "home_phone": self.home_phone,
            "mobile_phone": self.mobile_phone,
            "address": self.address,
            "address_2": self.address_2,
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


def requires_id(view):
    @wraps(view)
    def id_wrapper(*args, **kwargs):
        if "id" not in request.json:
            raise BadRequest("Field 'id' not found in request body")
        return view(*args, **kwargs)

    return id_wrapper


def validate_input_field_names(view):
    @wraps(view)
    def validate_wrapper(*args, **kwargs):
        json_data = request.json.copy()
        if "id" in request.json:
            json_data.pop("id")

        valid_fields = {
            "first_name",
            "last_name",
            "company",
            "email",
            "home_phone",
            "mobile_phone",
            "address",
            "address_2",
        }

        if not valid_fields.intersection(json_data) == json_data.keys():
            raise BadRequest(
                f"Json input was invalid, valid fields are {valid_fields}"
            )
        return view(*args, **kwargs)

    return validate_wrapper


def validate_query_field_names(view):
    @wraps(view)
    def validate_wrapper(*args, **kwargs):
        json_data = getattr(request, "json", None)
        valid_fields = {"company", "email"}

        if json_data and not (
            valid_fields.intersection(json_data) == json_data.keys()
        ):
            raise BadRequest(
                f"Query was invalid, valid fields are {valid_fields}"
            )
        return view(*args, **kwargs)

    return validate_wrapper


@app.route("/")
def hello():
    msg = success_resp_msg("contact-api by asyks, hello!")

    return jsonify(msg)


@app.route("/contact", methods=["GET"])
def get_one_contact():
    contact = Contact.get_single(id=request.json["id"])
    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contact/create", methods=["POST"])
@requires_auth
@validate_input_field_names
def create_contact():
    contact = Contact(
        **request.json,
        updated_by=request.authorization.username,
    )
    db.session.add(contact)
    db.session.commit()

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contact/update", methods=["PUT"])
@requires_auth
@requires_id
@validate_input_field_names
def update_contact():
    if "id" not in request.json:
        raise BadRequest("Field 'id' not found in request body")

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
@requires_id
def delete_contact():
    if "id" not in request.json:
        raise BadRequest("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json["id"])
    contact.updated_by = request.authorization.username
    contact.active = False
    db.session.commit()

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contacts", methods=["GET"])
@validate_query_field_names
def get_contacts():
    query_args = [Contact.active.is_(True)]

    if request.json:
        if "email" in request.json:
            query_args.append(Contact.email.like(request.json["email"]))
        if "company" in request.json:
            query_args.append(Contact.company.like(request.json["company"]))

    contacts = Contact.query.filter(*query_args).all()

    msg = success_resp_msg([contact.data_dict for contact in contacts])

    return jsonify(msg)


@app.errorhandler(BadRequest)
@app.errorhandler(InternalServerError)
@app.errorhandler(MethodNotAllowed)
@app.errorhandler(Unauthorized)
def handle_error(exception):
    err_msg = error_resp_msg(
        f"{exception.name}: {exception.description}"
    )
    response = jsonify(err_msg)
    response.status_code = exception.code

    return response
