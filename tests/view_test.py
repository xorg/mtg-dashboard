

def test_hello(client):
    response = client.get("/hello", content_type="html/text")

    assert response.status_code == 200
    assert response.data == b"Helllooooo"
