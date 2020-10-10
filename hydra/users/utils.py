"""Dependency and package import."""
from hydra import db, jwt
from flask_jwt_extended import create_access_token, current_user


# Define user loader function: to be called every time a protected route is
# accessed. Query may need to be modified


@jwt.user_loader_callback_loader
def userLoaderCallback(identity):
    """
    Query database for user id that matches passed id.

    If user does not exist, return None. Else, return the user.
    """
    user = db.users.find_one_or_404({"_id": identity})
    if identity not in user:
        return None
    return user
