import os
import pytest

from dotenv import load_dotenv

load_dotenv()

from mtg_dashboard import create_app
from mtg_dashboard.models import db

from sqlalchemy.sql import text

with open(
    os.path.join(os.path.dirname(__file__), "fixtures", "test_data.sql"), "rb"
) as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():

    app = create_app()
    app.config.from_object("mtg_dashboard.config.Test")
    db_path = app.config.get("SQLALCHEMY_DATABASE_URI").split("sqlite:///")[1]

    with app.app_context():
        # set up db
        db.create_all()

        # fill tables with test data
        with db.get_engine().connect() as c:
            for query in _data_sql.split("\n\n"):
                c.execute(text(query))

    yield app

    # clean up db
    with app.app_context():
        db.drop_all()
        os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
