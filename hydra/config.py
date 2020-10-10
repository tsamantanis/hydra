"""Dependency and package import."""
import os
from dotenv import load_dotenv


class Config(object):
    """Initialize environment variables."""

    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv("SECRET_KEY")

    # TODO: Below are for SMTP library if we choose to integrate forgot password functionality

    # MAIL_SERVER = "smtp.gmail.com"
    # MAIL_PORT = os.getenv("MAIL_PORT")
    # MAIL_USE_TTL = True
    # MAIL_USE_SSL = True
    # MAIL_DEBUG = True
    # MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    # MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    # MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    # MAIL_SUPPRESS_SEND = False
    # MAIL_ASCII_ATTACHMENTS = False

    # TODO: Will need these later for Stripe integration

    # STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLISHABLE")
    # STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False
