"""Dependency and package import."""
import os
from flask_pymongo import PyMongo
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from hydra.config import Config
import stripe

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
db = mongo.db
print(type(db))
jwt = JWTManager()

# use sk_test_51AQPwCHlrGbOVNVCu63XWCFDErvBRpBjUzQP825hGTcPvye0Eg0Lf4kOJW4mvEaHw7lSVxIpCOQRh887RGB74RRB00y5XZrF75
# their is a hard coded product that will store all pricing for diffrent courses
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


# TODO whereever we want to do the flask_login stuff we need to set the loginManagers load_user meathod
# @loginManager.user_loader
# def load_user(userId):
#     return db.User.find({'_id' : id(userId)})

CORS(app)

jwt.init_app(app)

from hydra.main.routes import main
from hydra.users.routes import users
from hydra.group.routes import groupBlueprint

# from hydra.groups.routes import groups
# TODO: continue route imports

app.register_blueprint(main, url_prefix="/")
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(groupBlueprint, url_prefix="/groups")

