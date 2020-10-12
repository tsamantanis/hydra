"""Dependency and package import."""
from flask import (
    Blueprint,
    request,
    url_for,
    jsonify,
)
from flask_login import login_required, login_user, logout_user, current_user
from hydra.users.utils import loadUser
from hydra.users.user import User
from hydra import db
from passlib.hash import sha256_crypt
from bson.json_util import dumps
import stripe

users = Blueprint("users", __name__)


# Helper function to identify blacklisted tokens
# This enables us to see tokens as revoked when a user logs out
# Can be made more robust to check for tokens we didn't create, possibly
# improve on later


#  TODO: do we need to return user to front end after sign up?


@users.route("/signup", methods=["GET", "POST"])
def signUp():
    """Sign up new user, add to DB, return new user object as JSON."""
    if request.method == "GET":
        return "hello", 200
    firstName = request.json.get("firstName")
    lastName = request.json.get("lastName")
    email = request.json.get("email")
    password = sha256_crypt.hash(request.json.get("password"))
    signUpUser = db.users.insert_one(
        {
            "firstName": firstName,
            "lastName": lastName,
            "email": email,
            "password": password,
        }
    )
    newUser = User(
        signUpUser.inserted_id, firstName, lastName, email, password
    )

    return dumps(newUser.id), 200


@users.route("/signin", methods=["POST"])
def signIn():
    """Sign in user."""
    email = request.json.get("email")
    password = request.json.get("password")
    user = db.users.find_one_or_404({"email": email})
    if not user:
        return (
            jsonify({"msg": "There is no user associated with that email."}),
            400,
        )
    if not sha256_crypt.verify(password, user["password"]):
        return jsonify({"msg": "Incorrect password entered."}), 400
    signInUser = User(
        user["_id"],
        user["firstName"],
        user["lastName"],
        user["email"],
        user["password"],
    )
    login_user(signInUser)
    return dumps(signInUser.id), 200


@users.route("/signout")
@login_required
def signOut():
    """Allow user to sign out."""
    if current_user.is_authenticated:
        logout_user()
    return jsonify({"msg": "Successfully logged out."}), 200


# TODO: further testing on this route
@users.route("/<user_id>", methods=["GET", "PUT", "POST"])
@login_required
def userProfile(user_id):
    """Provide data for user profile, editable by the user."""
    if request.method == "GET":
        return jsonify(
            email=current_user.email,
            firstName=current_user.firstName,
            lastName=current_user.lastName,
        )
    if request.method == "PUT":
        newFirstName = request.json.get("firstName")
        newLastName = request.json.get("lastName")
        newEmail = request.json.get("email")
        updated_user = db.users.update(
            {"_id": current_user.id},
            {
                "$set": {
                    "firstName": newFirstName,
                    "lastName": newLastName,
                    "email": newEmail,
                }
            },
        )
        return jsonify(
            {
                "firstName": newFirstName,
                "lastName": newLastName,
                "email": newEmail,
            }
        )
    if request.method == "POST":
        # TODO: handle image uploading
        pass


@users.route("/payments")
@login_required
def userPayments():
    """
    Return user payment methods stored through Stripe.

    Segment of payment info revealed to us through Stripe API for UI.
    """
    return stripe.paymentMethod.retrieve(f"{current_user.stripeId}")


# TODO: update values based on client side input/form (stripe specific?)
# Should we be hashing these values so that the plaintext isn't coming through?


@users.route("/addpayment", methods=["POST"])
@login_required
def userAddPayment():
    """Allow user to add payment method for subscription."""
    cardNumber = request.json.get("cardNumber")
    expMonth = request.json.get("expMonth")
    expYear = request.json.get("expYear")
    cvc = request.json.get("cvc")
    addressCity = request.json.get("city")
    addressCountry = request.json.get("country")
    addressLineOne = request.json.get("lineOne")
    addressLineTwo = request.json.get("lineTwo", None)
    postalCode = request.json.get("postalCode")
    state = request.json.get("state")
    stripe.PaymentMethod.create(
        type="card",
        card={
            "number": {{cardNumber}},
            "exp_month": {{expMonth}},
            "exp_year": {{expYear}},
            "cvc": {{cvc}},
        },
        billing_details={
            "address": {
                "city": {{addressCity}},
                "country": {{addressCountry}},
                "line1": {{addressLineOne}},
                "line2": {{addressLineTwo}},
                "postal_code": {{postalCode}},
                "state": {{state}},
            },
            "email": {{current_user.email}},
            "name": {{current_user.name}},
        },
    )
    return stripe.paymentMethod, 200


# User requests reset token


@users.route("/passwordreset/sendtoken", methods=["POST"])
def resetRequest():
    """Return message for front-end."""
    email = request.json.get("email")
    user = db.users.find_one_or_404({"email": email})
    if not user:
        return (
            jsonify(
                {
                    "msg": "There is no account associated with that email address."
                }
            ),
            400,
        )
    sendResetEmail(user)
    return (
        jsonify(
            {
                "msg": "An email has been sent with a link to reset your password."
            }
        ),
        200,
    )


@users.route("/passwordreset/<token>")
def verifyResetTokenView(token):
    """Verify reset token from user to reset password."""
    user = User.verifyResetToken(token)
    if not user:
        return jsonify({"msg": "Token is invalid or expired."})
    newPassword = sha256_crypt.hash(request.json.get("newPassword"))
    updatedUser = db.users.update_one(
        {"_id": ObjectId(user.id)},
        {"$set": {"password": newPassword}},
    )
    return jsonify({"msg": "Your password has been updated."}), 200
