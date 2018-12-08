from functools import wraps
import os

from flask import request

from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import Unauthorized


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
            "phone",
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
