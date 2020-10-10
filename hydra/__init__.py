"""Dependency and package import."""
import os
import pymongo
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from hydra.config import Config
import stripe

client = pymongo.MongoClient(os.getenv("DATABASE_URL"))
db = client.test

# use sk_test_51AQPwCHlrGbOVNVCu63XWCFDErvBRpBjUzQP825hGTcPvye0Eg0Lf4kOJW4mvEaHw7lSVxIpCOQRh887RGB74RRB00y5XZrF75
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# TODO whereever we want to do the flask_login stuff we need to set the loginManagers load_user meathod
# @loginManager.user_loader
# def load_user(userId):
#     return db.User.find({'_id' : id(userId)})


def create_app(config_class=Config):
    """Return app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    jwt = JWTManager(app)

    from hydra.main.routes import main
    from hydra.users.routes import users

    # from hydra.groups.routes import groups
    # TODO: continue route imports

    app.register_blueprint(main)
    app.register_blueprint(user)

    return app
