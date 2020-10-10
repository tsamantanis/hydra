"""Dependency and package import."""
import os
import pymongo
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from hydra.config import Config


def create_app(config_class=Config):
    """Return app."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    client = pymongo.MongoClient(os.getenv("DATABASE_URL"))
    db = client.test

    jwt = JWTManager(app)

    from hydra.main.routes import main
    from hydra.user.routes import user

    # from hydra.groups.routes import groups
    # TODO: continue route imports

    app.register_blueprint(main)
    app.register_blueprint(user)

    return app
