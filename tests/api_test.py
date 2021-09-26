import json
from mtg_dashboard.models import Card, Collection


def test_cards(app, client):
    """Test card endpoint"""
    with app.app_context():
        response = client.get("/api/cards", content_type="text/json")

        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == len(Card.query.all())

        card = Card.query.filter(Card.name == "Mother of Runes")[0]
        assert data[0]["name"] == card.name
        assert data[0]["current_price"] == card.current_price
        assert len(data[0]["prices"]) == len(card.prices)


def test_collections(app, client):
    """Test collection endpoint"""
    with app.app_context():
        response = client.get("/api/collections", content_type="text/json")
        data = json.loads(response.data)

        assert response.status_code == 200
        assert len(data) == len(Collection.query.all())

        col1 = Collection.query.filter(Collection.name == "Collection 1")[0]
        assert data[0]["name"] == col1.name
        assert data[0]["value"] == col1.value


def test_collection_detail(app, client):
    """Test collection detail endpoint"""
    with app.app_context():
        response = client.get("/api/collections/1", content_type="text/json")
        data = json.loads(response.data)
        assert response.status_code == 200
        col1 = Collection.query.filter(Collection.name == "Collection 1")[0]

        assert data["name"] == col1.name
        assert data["value"] == col1.value
        assert type(data['history']) == list
