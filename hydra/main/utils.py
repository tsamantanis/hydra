"""Dependency and package import."""
from flask import request, g, abort
from jwt import decode, exceptions
from functools import wraps
import json

# Overwrite the flask-login login_required decorator to return
# better data types, handle redirects on front end for better UI/UX


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        authorization = request.headers.get("authorization", None)
        if not authorization:
            return (
                json.dumps({"error": "no authorization token provied"}),
                403,
                {"Content-type": "application/json"},
            )

        try:
            token = authorization.split(" ")[1]
            resp = decode(token, None, verify=False, algorithms=["HS256"])
            g.user = resp["sub"]
        except exceptions.DecodeError as identifier:
            return (
                json.dumps({"error": "invalid authorization token"}),
                403,
                {"Content-type": "application/json"},
            )

        return f(*args, **kwargs)

    return wrap
