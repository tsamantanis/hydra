"""Dependency and package import."""
from flask import request, g, abort
from jwt import decode, exceptions
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hydra import app
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


# Define function to create verification token for pass reset


def get_reset_token(userId, expires_sec=900):
    """Enable 'forgot password' functionality."""
    s = Serializer(app.config["SECRET_KEY"], expires_sec)
    return s.dumps({"user_id": userId}).decode("utf-8")


# Define function to validate verification token
