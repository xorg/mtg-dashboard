import os
import pytest

from dotenv import load_dotenv
load_dotenv()

from mtg_dashboard import create_app
from mtg_dashboard.models import db


@pytest.fixture
def app():

    app = create_app()
    app.config.from_object('mtg_dashboard.config.Test')

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()
        db_path = app.config.get('SQLALCHEMY_DATABASE_URI').split("sqlite:///")[1]
        os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
