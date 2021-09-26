from flask import Blueprint
from flask import jsonify
from mtg_dashboard.models import Collection, Price, Card

api_bp = Blueprint("api", __name__)


# view all collections
@api_bp.route("/api/collections", methods=["GET"])
def collections():
    collections = Collection.query.all()
    return jsonify(collections)


# view price history of one collection
@api_bp.route("/api/collections/<int:id>", methods=["GET"])
def collection_detail(id):
    collection = Collection.query.filter(Collection.id == id).first()

    col = {
        "name": collection.name,
        "value": collection.value,
        "history": collection.value_history,
        "cards": list(collection.cards),
    }
    return jsonify(col)


# view all cards
@api_bp.route("/api/cards", methods=["GET"])
def cards():
    cards = Card.query.all()
    return jsonify(list(cards))


# view all cards
# accepts ?range=1d param
@api_bp.route("/api/cards/trending", methods=["GET"])
def cards_trending():
    cards = Card.query.join(Price)
    return jsonify(list(cards))


# specific card with prices
@api_bp.route("/api/cards/<int:id>", methods=["GET"])
def card(id):
    card = Card.query.filter_by(id=id).first()
    card.prices = Price.query.filter_by(card_id=id).all()
    print(card.prices)
    return jsonify(card)


# view prices of a card by id
@api_bp.route("/api/cards/<int:card_id>/price", methods=["GET"])
def card_prices(card_id):
    card_price_query = (
        Price.query.filter_by(card_id=card_id).order_by(Price.date.asc()).all()
    )
    return jsonify(card_price_query)
