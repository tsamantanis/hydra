"""Dependency and package import."""
from flask import Blueprint, render_template, request, url_for, redirect
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
)
main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Return homepage."""
    return "You are home."
