"""Dependency and package import."""
from hydra import db, jwt
from flask import url_for
from flask_jwt_extended import create_access_token, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hydra.users.send_mail import sendMail
from hydra import app


# Define user loader function: to be called every time a protected route is
# accessed. Query may need to be modified


@jwt.user_loader_callback_loader
def userLoaderCallback(identity):
    """
    Query database for user id that matches passed id.

    If user does not exist, return None. Else, return the user.
    """
    currentUser = db.users.find_one_or_404({"_id": identity})
    if identity not in currentUser:
        return None
    return currentUser


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
