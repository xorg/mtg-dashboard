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


def test_cards_most_valued(app, client):
    """Test most_valued parameter"""
    with app.app_context():
        response = client.get("/api/cards?order_by=value", content_type="text/json")

        data = json.loads(response.data)
        assert response.status_code == 200
        assert data[0]["current_price"] == 4.99
        assert data[1]["name"] == "Fencing Ace"


def test_cards_limit(app, client):
    """Test limit parameter"""
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
        assert type(data["history"]) == list


def test_stats_endpoint(app, client):
    """Test collection detail endpoint"""
    with app.app_context():
        response = client.get("/api/stats", content_type="text/json")
        data = json.loads(response.data)
        assert response.status_code == 200

        # test 'Number of cards' stat
        assert data[0]["number"] == len(Card.query.all())

        # test 'Number of collections' stat
        assert data[1]["number"] == len(Collection.query.all())

        # test 'Average collection value' stat
        avg_value = int(sum([c.value for c in Collection.query.all()]) / len(Collection.query.all()))
        assert data[2]["number"] == f"{avg_value}$"

        # test 'Max card value' stat
        max_value = Card.query.where(Card.current_price > 0).order_by(Card.current_price.desc()).first().current_price
        assert (
            data[3]["number"] == f"{max_value}$"
        )
