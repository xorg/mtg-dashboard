import json
from mtg_dashboard.models import Card, Collection


def test_cards(app, client):
    """Test card endpoint"""
    with app.app_context():
        response = client.get("/api/cards", content_type="text/json")

        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == len(Card.query.all())

        card = Card.query.filter(Card.name == "Adanto Vanguard")[0]
        assert data[1]["name"] == card.name
        assert data[1]["current_price"] == card.current_price
        assert len(data[1]["prices"]) == len(card.prices)


def test_cards_most_valued(app, client):
    """Test most_valued parameter"""
    with app.app_context():
        response = client.get("/api/cards?most_valued=1", content_type="text/json")

        data = json.loads(response.data)
        assert response.status_code == 200
        assert data[0]["current_price"] == 4.99
        assert data[1]["name"] == 'Fencing Ace'


def test_cards_limit(app, client):
    """Test most_valued parameter"""
    with app.app_context():
        response = client.get("/api/cards?limit=1", content_type="text/json")

        data = json.loads(response.data)
        assert response.status_code == 200
        assert len(data) == 1


def test_card_detail(app, client):
    """Test card detail endpoint"""
    with app.app_context():
        response = client.get("/api/cards/1", content_type="text/json")
        data = json.loads(response.data)
        assert response.status_code == 200
        card = Card.query.filter(Card.name == "Mother of Runes")[0]

        assert data["name"] == card.name
        assert data["current_price"] == card.current_price
        assert type(data['prices']) == list


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
