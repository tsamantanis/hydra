"""Dependency and package import."""
from flask import Blueprint, render_template, request, url_for, redirect

# TODO: from hydra import db

user = Blueprint("user", __name__)


@user.route("/user/signUp")
def signUp():
    """Sign up new user, add to DB."""
    pass


@user.route("/user/signIn")
def signIn():
    """Sign in user."""
    pass


@user.route("/user/signOut")
def signOut():
    """Allow user to sign out."""
    pass


@user.route("/user/<user_id>")
def userProfile():
    """Provide data for user profile, editable by the user."""
    pass


@user.route("/user/payments")
def userPayments():
    """
    Return user payment methods stored through Stripe.

    Segment of payment info revealed to us through Stripe API for UI.
    """
    pass


@user.route("/user/addPayment")
def userAddPayment():
    """Allow user to add payment method for subscription."""
    pass
