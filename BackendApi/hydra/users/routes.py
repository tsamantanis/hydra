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
    password = sha256_crypt.hash(request.json.get("password"))
    newUser = User(123, firstName, lastName, email, password)
    insertUser = {
        "firstName": newUser.firstName,
        "lastName": newUser.lastName,
        "email": newUser.email,
        "password": newUser.password,
    }
    signUpUser = db.users.insert_one(insertUser)
    return jsonify({"msg": "Sign Up successful."}), 200


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
    userIdToString = str(user["_id"])
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


# TODO: further testing on this route
@users.route("/<user_id>", methods=["GET", "PUT", "POST"])
@jwt_required
def userProfile(user_id):
    """Provide data for user profile, editable by the user."""
    print("In user profile end")
    currentUser = get_jwt_identity()
    print(f"Current user after calling get identity {currentUser}")
    currentUser = userLoaderCallback(user_id)
    print(f"Current user after calling user loader cb {currentUser}")
    if request.method == "GET":
        return jsonify(
            email=currentUser.email,
            firstName=currentUser.firstName,
            lastName=currentUser.lastName,
            bio=currentUser.bio,
        )
    if request.method == "PUT":
        jsonSet = {}
        if request.json.get("bio") != None:
            jsonSet["firstName"] = request.json.get("firstName")
        if request.json.get("bio") != None:
            jsonSet["lastName"] = request.json.get("lastName")
        if request.json.get("bio") != None:
            jsonSet["email"] = request.json.get("email")
        if request.json.get("bio") != None:
            jsonSet["password"] = request.json.get("password")
        if request.json.get("bio") != None:
            jsonSet["bio"] = request.json.get("bio")

        db.User.update(
                    { '_id': currentUser['_id'] },
                    { '$set':
                        jsonSet
                    }
                )
        return 'User Updated', 200
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
    number = request.json.get("number")
    expMonth = request.json.get("country")
    cardNumber = request.json.get("line1")
    expMonth = request.json.get("line2")
    cardNumber = request.json.get("cardNumber")
    expMonth = request.json.get("expMonth")
    stripe.PaymentMethod.create(
        type="card",
        card={
            "number": request.json.get("number"),
            "exp_month": request.json.get("exp_month"),
            "exp_year": request.json.get("exp_year"),
            "cvc": request.json.get("cvc"),
        },
        billing_details={
            "address": {
                "city": request.json.get("city"),
                "country": request.json.get("country"),
                "line1": request.json.get("address").get('line1'),
                "line2": request.json.get("address").get('line2'),
                "postal_code": request.json.get("address").get('postal_code'),
                "state": request.json.get("address").get('state')
            },
            "name": request.json.get("name"),
        },
    )
    return stripe.paymentMethod, 200


# User requests reset token

# TODO: More testing on this route. I
# Literally do not understand why I'm getting an error
# from sign in on this route. fix tomorrow.


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
