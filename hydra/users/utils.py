"""Dependency and package import."""
from flask import request, g, abort
from hydra import db, jwt
from jwt import decode, exceptions
from flask_jwt_extended import user_loader_callback_loader
from functools import wraps
import json

# Using JSON Web Tokens as opposed to Flask-Login for ease of use on the
# front-end


def login_required(f):
    """Wrap route function with login_required to require authentication to access."""

    @wraps(f)
    def wrap(*args, **kwargs):
        authorization = request.headers.get("authorization", None)
        if not authorization:
            return (
                json.dumps({"error": "no authorization token provided"}),
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


# Define user loader function: to be called every time a protected route is
# accessed. Query may need to be modified


@jwt.user_loader_callback_loader
def userLoaderCallback(identity):
    """
    Query database for user id that matches passed id.

    If user does not exist, return None. Else, return the user.
    """
    user = db.users.find_one_or_404({"_id": identity})
    if identity not in user:
        return None
    return user
