import os
os.environ["FLASK_ENV"] = "test"
from mtg_dashboard import app


def test_hello():
    tester = app.test_client()
    response = tester.get("/hello", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"Helllooooo"
