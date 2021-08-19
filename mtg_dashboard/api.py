from flask import Blueprint
from flask import jsonify
from mtg_dashboard.models import Collection, Price, Card, db

api_bp = Blueprint("api", __name__)


# view all collections
@api_bp.route("/api/collections", methods=["GET"])
def collections():
    collections = Collection.query.all()
    return jsonify(collections)


# view price history of one collection
@api_bp.route("/api/collections/<int:id>", methods=["GET"])
def collection_detail(id):
    collection = Collection.query.get(id)
    query = collection.value_history()
    res = db.session.execute(query)
    value_history = [tuple(i) for i in res]
    col = {
        "name": collection.name,
        "value": collection.value,
        "history": value_history,
        "cards": list(collection.cards),
    }
    return jsonify(col)


# view all cards
@api_bp.route("/api/cards", methods=["GET"])
def cards():
    cards = Card.query.filter(Card.current_price > 10.0)
    return jsonify(list(cards))


# specific card with prices
@api_bp.route("/api/card/<int:id>", methods=["GET"])
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
