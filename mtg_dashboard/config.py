import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    FLASK_APP = os.environ["FLASK_APP"]
    try:
        SECRET_KEY = os.environ["SECRET"]
    except KeyError:
        SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Production(Config):
    DEBUG = False


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True


class Test(Config):
    # use sqlite db for testing for easier test db setup
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/test.sqlite"
    TESTING = True
