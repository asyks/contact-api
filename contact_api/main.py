from flask import Flask
from flask import jsonify
from flask import request

from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import InternalServerError
from werkzeug.exceptions import MethodNotAllowed


app = Flask(__name__)

app.config.update({
    "SQLALCHEMY_DATABASE_URI": "sqlite://",
    "SQLALCHEMY_TRACK_MODIFICATIONS": True,
    "DEBUG": True,
})

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    company = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(120), nullable=False)

    @property
    def data_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "email": self.email,
        }

    @classmethod
    def get_single(cls, **kwargs):
        inst = cls.query.filter_by(**kwargs).first()
        if not inst:
            raise InternalServerError("Contact does not exist")

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


@app.route("/")
def hello():
    msg = success_resp_msg("contact-api by asyks")

    return jsonify(msg)


@app.route("/contact", methods=["GET"])
def get_one_contact():
    if "id" not in request.json:
        raise InternalServerError("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json['id'])

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contact/create", methods=["POST"])
def create_contact():
    contact = Contact(
        name=request.json["name"],
        company=request.json["company"],
        email=request.json["email"],
    )
    db.session.add(contact)
    db.session.commit()

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contact/update", methods=["PUT"])
def update_contact():
    if "id" not in request.json:
        raise InternalServerError("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json['id'])

    if "name" in request.json:
        contact.name = request.json["name"]
    if "company" in request.json:
        contact.name = request.json["company"]
    if "email" in request.json:
        contact.email = request.json["email"]

    db.session.commit()

    msg = success_resp_msg(contact.data_dict)
    response = jsonify(msg)
    response.status_code = 201

    return response


@app.route("/contact/delete", methods=["DELETE"])
def delete_contact():
    if "id" not in request.json:
        raise InternalServerError("Field 'id' not found in request body")

    contact = Contact.get_single(id=request.json['id'])
    db.session.delete(contact)
    db.session.commit()

    msg = success_resp_msg(contact.data_dict)

    return jsonify(msg)


@app.route("/contacts", methods=["GET"])
def get_contacts():
    if request.json:
        contacts = Contact.query.filter_by(**request.json).all()
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


@app.errorhandler(InternalServerError)
@app.errorhandler(MethodNotAllowed)
def handle_error(exception):
    err_msg = error_resp_msg(
        f"{exception.name}: {exception.description}"
    )
    response = jsonify(err_msg)
    response.status_code = exception.code

    return response
