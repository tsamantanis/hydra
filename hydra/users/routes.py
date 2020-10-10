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
    get_raw_jwt,
)
from hydra.users.utils import userLoaderCallback
from hydra.users.user import User
from passlib.hash import sha256_crypt
from hydra import db, jwt

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


@users.route("/users/signUp", methods=["POST"])
def signUp():
    """Sign up new user, add to DB, return new user object as JSON."""
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    email = request.form.get("email")
    password = sha256_crypt.hash(request.form.get("password"))
    newUser = User(firstName, lastName, email, password)
    signUpUser = db.users.insert_one(newUser)
    return jsonify(signUpUser), 200


@users.route("/users/signIn", methods=["POST"])
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


# Revoke current user token, logging them out.
@users.route("/users/signOut")
@jwt_required
def signOut():
    """Allow user to sign out."""
    jti = get_raw_jwt()["jti"]
    db.blacklist.insert_one(jti)
    return jsonify({"msg": "Successfully logged out."}), 200


@users.route("/users/<user_id>", methods=["GET", "PUT", "POST"])
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
        bio = request.form.get("bio")
        newFirstName = request.form.get("firstName")
        newLastName = request.form.get("lastName")
        return jsonify(firstName=newFirstName, lastName=newLastName, bio=bio)
    if request.method == "POST":
        # TODO: handle image uploading
        pass


@users.route("/users/payments")
def userPayments():
    """
    Return user payment methods stored through Stripe.

    Segment of payment info revealed to us through Stripe API for UI.
    """
    pass


@users.route("/users/addPayment")
def userAddPayment():
    """Allow user to add payment method for subscription."""
    pass
