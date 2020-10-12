"""Dependency and package import."""
from hydra import db
from flask import url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from hydra.users.send_mail import sendMail
from hydra import app, loginManager


# Define user loader function: to be called every time a protected route is
# accessed. Query may need to be modified


@loginManager.user_loader
def loadUser(id):
    """Define user callback for user_loader function."""
    return db.users.find_one_or_404({"_id": id})


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
