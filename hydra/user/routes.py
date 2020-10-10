"""Dependency and package import."""
from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    jsonify,
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
)
from hydra.user import utils
from passlib.hash import sha256_crypt
from hydra import db

user = Blueprint("user", __name__)


@user.route("/user/signUp", methods=["POST"])
def signUp():
    """Sign up new user, add to DB, return new user object as JSON."""
    firstName = request.form.get("first-name")
    lastName = request.form.get("last-name")
    email = request.form.get("email")
    password = sha256_crypt.hash(request.form.get("password"))
    newUser = {
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "password": password,
    }
    signUpUser = db.users.insert_one(newUser)
    return jsonify(signUpUser), 200


@user.route("/user/signIn", methods=["POST"])
def signIn():
    """Sign in user."""
    email = request.form.get("email")
    password = request.form.get("password")
    user = db.users.find_one_or_404({"email": email})
    if not user:
        return (
            jsonify({"msg": "There is no user associated with that email."}),
            400,
        )
    if password != sha256_crypt.verify(user.password):
        return jsonify({"msg": "Incorrect password entered."}), 400
    accessToken = create_access_token(identity=user.id)
    return jsonify(accessToken=accessToken), 200


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
