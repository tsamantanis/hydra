"""Dependency and package import."""
from flask import Blueprint, render_template, request, url_for, redirect

main = Blueprint("main", __name__)


@main.route("/")
def home():
    """Return homepage."""
    return "You are home."
