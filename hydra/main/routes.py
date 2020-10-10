"""Dependency and package import."""
from flask import Blueprint, render_template, request, url_for, redirect

# TODO:
# from hydra import db

main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Return homepage."""
    return render_template("index.html")
