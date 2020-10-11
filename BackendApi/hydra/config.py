"""Dependency and package import."""
import os, json

class Config(object):
    """Initialize environment variables."""
    config = None
    with open(os.path.join(os.getcwd(), 'BackendApi/app.config')) as config_file:
        config = json.load(config_file)

    DEBUG = False
    TESTING = False

    SECRET_KEY = config.get("SECRET_KEY")
    MONGO_URI = config.get("DATABASE_URL")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = config.get("MAIL_PORT")
    MAIL_USE_TTL = True
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = config.get("MAIL_USERNAME")
    MAIL_PASSWORD = config.get("MAIL_PASSWORD")
    # MAIL_DEFAULT_SENDER = os.get("MAIL_DEFAULT_SENDER")
    MAIL_SUPPRESS_SEND = False
    MAIL_ASCII_ATTACHMENTS = False

    # TODO: Will need these later for Stripe integration

    # STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLISHABLE")
    # STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False
