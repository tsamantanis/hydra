"""Dependency and package import."""
from flask import (
    Blueprint,
    request,
    url_for,
    jsonify,
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt,
)

from hydra.users.utils import userLoaderCallback, sendResetEmail
from hydra.users.user import User
from hydra import db, jwt
from passlib.hash import sha256_crypt
import stripe

users = Blueprint("users", __name__)


# Helper function to identify blacklisted tokens
# This enables us to see tokens as revoked when a user logs out
# Can be made more robust to check for tokens we didn't create, possibly
# improve on later


@jwt.token_in_blacklist_loader
def checkIfTokenInBlacklist(decryptedToken):
    """Check if token is in blacklist. Return blacklisted token."""
    jti = decryptedToken["jti"]
    return jti in db.blacklist.find_all({"decrypt": jti})


# TODO: re-implement password hashing after debugging


@users.route("/signup", methods=["GET", "POST"])
def signUp():
    """Sign up new user, add to DB, return new user object as JSON."""
    if request.method == "GET":
        return "hello", 200
    firstName = request.json.get("firstName")
    lastName = request.json.get("lastName")
    email = request.json.get("email")
    password = request.json.get("password")
    newUser = User(firstName, lastName, email, password)
    insertUser = {
        "firstName": newUser.firstName,
        "lastName": newUser.lastName,
        "email": newUser.email,
        "password": newUser.password,
    }
    signUpUser = db.users.insert_one(insertUser)
    return jsonify({"msg": "POST method successful"}), 200


@users.route("/signin", methods=["POST"])
def signIn():
    """Sign in user."""
    email = request.json.get("email")
    password = request.json.get("password")
    print(f"Password: {password}")
    user = db.users.find_one_or_404({"email": email})
    print(f"User from db: {user}")
    if not user:
        return (
            jsonify({"msg": "There is no user associated with that email."}),
            400,
        )
    if password != user["password"]:
        return jsonify({"msg": "Incorrect password entered."}), 400
    print(f"User id before stringified: {user['_id']}")
    userIdToString = str(user["_id"])
    print(userIdToString)
    accessToken = create_access_token(identity=userIdToString)
    return jsonify({"accessToken": accessToken}), 200


# Revoke current user token, logging them out.
@users.route("/signout")
@jwt_required
def signOut():
    """Allow user to sign out."""
    jti = get_raw_jwt()["jti"]
    db.blacklist.insert_one(jti)
    return jsonify({"msg": "Successfully logged out."}), 200


@users.route("/<user_id>", methods=["GET", "PUT", "POST"])
@jwt_required
def userProfile():
    """Provide data for user profile, editable by the user."""
    currentUser = get_jwt_identity()
    userLoaderCallback(currentUser)
    if request.method == "GET":
        return jsonify(
            email=currentUser.email,
            firstName=currentUser.firstName,
            lastName=currentUser.lastName,
            bio=currentUser.bio,
        )
    if request.method == "PUT":
        bio = request.json.get("bio")
        newFirstName = request.json.get("firstName")
        newLastName = request.json.get("lastName")
        return jsonify(
            {"firstName": newFirstName, "lastName": newLastName, "bio": bio}
        )
    if request.method == "POST":
        # TODO: handle image uploading
        pass


@users.route("/payments")
@jwt_required
def userPayments():
    """
    Return user payment methods stored through Stripe.

    Segment of payment info revealed to us through Stripe API for UI.
    """
    currentUser = get_jwt_identity()
    userLoaderCallback(currentUser)
    return stripe.paymentMethod.retrieve(f"{currentUser.stripeId}")


# TODO: update values based on client side input/form (stripe specific?)
# Should we be hashing these values so that the plaintext isn't coming through?


@users.route("/addpayment", methods=["POST"])
@jwt_required
def userAddPayment():
    """Allow user to add payment method for subscription."""
    currentUser = get_jwt_identity()
    userLoaderCallback(currentUser)
    cardNumber = request.json["cardNumber"]
    expMonth = request.json["expMonth"]
    stripe.PaymentMethod.create(
        type="card",
        card={
            "number": None,
            "exp_month": None,
            "exp_year": None,
            "cvc": None,
        },
        billing_details={
            "address": {
                "city": None,
                "country": None,
                "line1": None,
                "line1": None,
                "postal_code": None,
                "state": None,
            },
            "email": None,
            "name": None,
        },
    )
    return stripe.paymentMethod, 200


# User requests reset token


@users.route("/resetpassword", methods=["POST"])
def resetRequest():
    """Return message for front-end."""
    email = request.json["email"]
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


@users.route("/resetpassword/<token>")
def verifyResetToken(token):
    """Verify reset token from user to reset password."""
    user = User.verifyResetToken(token)
    if not user:
        return jsonify({"msg": "Token is invalid or expired."})
    newPassword = sha256_crypt.hash(request.json["newPassword"])
    updatedUser = db.users.update_one(
        {"_id": ObjectId(user.id)},
        {"$set": {"password": newPassword}},
    )
    return jsonify({updatedUser}), 200
