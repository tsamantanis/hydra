"""Dependency and package import."""
from hydra import db
from flask import url_for, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hydra.users.send_mail import sendMail
from hydra.users.user import User
from passlib.hash import sha256_crypt
from bson.json_util import dumps
from bson.objectid import ObjectId
from hydra import app, loginManager
import os


# Define user loader function: to be called every time a protected route is
# accessed. Query may need to be modified

#
# @loginManager.user_loader
# def loadUser(id):
#     """Define user callback for user_loader function."""
#     return db.users.find_one_or_404({"_id": id})


@loginManager.request_loader
def loadUserToken(request):
    """Verify the token passed from request."""
    s = Serializer(os.getenv("SECRET_KEY"))
    token = request.headers.get("Authorization")
    if token is None:
        return jsonify({"msg": "Missing authoriation token."}), 405

    elif token is not None:
        credential = token
        user = db.users.find_one_or_404({"authToken": credential})
        authenticatedUser = User(
            user["_id"],
            credential,
            user["firstName"],
            user["lastName"],
            user["email"],
            user["password"],
        )
        return authenticatedUser


def createToken(email, password):
    """Create token for client side authentication and tracking."""
    user_entry = db.users.find_one_or_404({"email": email})
    if user_entry is not None:
        if sha256_crypt.verify(password, user_entry["password"]):
            token = f"Bearer {user_entry['_id']}"
            authorizedUser = db.users.update_one(
                {"_id": ObjectId(user_entry["_id"])},
                {"$set": {"authToken": token}},
            )
            user = User(
                user_entry["_id"],
                token,
                user_entry["firstName"],
                user_entry["lastName"],
                user_entry["email"],
                user_entry["password"],
            )
            return (
                dumps(
                    {
                        "userId": user_entry["_id"],
                        "authToken": token,
                        "firstName": user_entry["firstName"],
                        "lastName": user_entry["lastName"],
                        "email": user_entry["email"],
                    }
                ),
                user,
                token,
            )
    return jsonify({"msg": "No user found, check your credentials."})


# Define functions to send user reset password tokens


def getResetToken(user, expires_sec=900):
    """Enable 'forgot password' functionality."""
    s = Serializer(app.config["SECRET_KEY"], expires_sec)
    return s.dumps({"user_id": user["_id"]}).decode("utf-8")


def verifyResetToken(token):
    """Verify that the user enters the correct pass reset token."""
    s = Serializer(app.config["SECRET_KEY"])
    try:
        userId = s.loads(token)["user_id"]
    except:
        return None
    return db.users.find_one_or_404({"_id": userId})


def sendResetEmail(user):
    """Send password reset email."""
    token = getResetToken(user)
    msg = f"""
                To reset your password, please click the following link:
                {url_for('verifyResetTokenView', token=token, _external=True)}
                If you did not make this request, please ignore this email."""
    sendMail("Reset Password", msg, user["email"])
