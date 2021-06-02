from flask import Blueprint
from flask import jsonify
from mtg_dashboard.models import Collection, Price, Card

api_bp = Blueprint("api", __name__)


# view all collections
@api_bp.route("/collection", methods=["GET"])
def collections():
    collections = Collection.query.all()
    return jsonify(collections)


# view all cards
@api_bp.route("/api/card", methods=["GET"])
def cards():
    cards = Card.query.all()
    return jsonify(cards)


# view prices of a card by id
@api_bp.route("/api/card/<int:card_id>/price", methods=["GET"])
def card_prices(card_id):
    card_price_query = Price.query.filter_by(card_id=card_id).order_by(Price.date.asc()).all()
    return jsonify(card_price_query)


@api_bp.route("/api/price", methods=["GET"])
def price():
    price = Price.query.order_by(Price.price.desc()).all()
    return jsonify(price)


