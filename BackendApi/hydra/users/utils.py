"""Dependency and package import."""
from hydra import db, jwt
from flask import url_for
from flask_jwt_extended import create_access_token, current_user
from hydra.users.send_mail import sendMail


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


# Define function to send user reset password tokens


def sendResetEmail(user):
    """Send password reset email."""
    token = user.getResetToken()
    msg = f"""
                To reset your password, please click the following link:
                {url_for('reset_token', token=token, _external=True)}
                If you did not make this request, please ignore this email."""
    sendMail("Reset Password", msg, user.email)
