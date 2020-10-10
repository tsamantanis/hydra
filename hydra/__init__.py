"""Dependency and package import."""
import os
import pymongo
from flask import Flask
from flask_login import LoginManager
from hydra.config import Config

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"


def create_app(config_class=Config):
    """Return app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)

    client = pymongo.MongoClient(os.getenv("DATABASE_URL"))
    db = client.test

    from hydra.main.routes import main
    from hydra.users.routes import users

    # from hydra.groups.routes import groups
    # TODO: continue route imports

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
