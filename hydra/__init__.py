"""Dependency and package import."""
import os
from flask import Flask
from hydra.config import Config

# TODO: Set up database

# db =

# TODO: Set up Flask-Login

# login_manager = LoginManager(app)
# login_manager.session_protection = "strong"
# login_manager.login_view = "login"


def create_app(config_class=Config):
    """Function to create app."""

    app = Flask(__name__)
    app.config.from_object(config_class)
    # login_manager.init_app(app)

    from hydra.main.routes import main
    from hydra.users.routes import users

    # from hydra.groups.routes import groups
    # TODO: continue route imports

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
