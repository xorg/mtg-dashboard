from flask import Blueprint
from flask import jsonify
from mtg_dashboard.models import Collection, Price, Card

api_bp = Blueprint("api", __name__)


# view all collections
@api_bp.route("/collections", methods=["GET"])
def collections():
    collections = Collection.query.all()
    return jsonify(collections)


@api_bp.route("/cards", methods=["GET"])
def cards():
    cards = Card.query.all()
    return jsonify(cards)


@api_bp.route("/prices", methods=["GET"])
def price():
    price = Price.query.all()
    return jsonify(price)
