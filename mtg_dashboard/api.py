from flask import Blueprint
from flask import jsonify
from flask import request
from mtg_dashboard.models import Collection, Card

api_bp = Blueprint("api", __name__)


# view all collections
@api_bp.route("/api/collections", methods=["GET"])
def collections():
    """View list of all collections

    Returns:
        A list of all collections in database
    """
    collections = Collection.query.all()
    return jsonify(collections)


@api_bp.route("/api/collections/<int:id>", methods=["GET"])
def collection_detail(id):
    """View detailed collection object with aggregated price hisory

    Args:
        id: ID of collection to display

    Returns:
        A json object with all detail information of the given collection
    """
    collection = Collection.query.filter(Collection.id == id).first()

    col = {
        "name": collection.name,
        "value": collection.value,
        "history": collection.value_history,
        "cards": list(collection.cards),
    }
    return jsonify(col)


@api_bp.route("/api/cards", methods=["GET"])
def cards():
    """List all cards

    Parameters:
    most_valued: sort by value
    limit: only display <limit> entries

    Returns:
        A json list of all cards in database
    """
    cards = list(Card.query.all())
    most_valued = request.args.get("most_valued")
    if most_valued:
        cards = sorted(cards, key=lambda x: x.current_price, reverse=True)

    limit = request.args.get("limit")
    print(limit)
    cards = cards[:int(limit)] if limit else cards

    return jsonify(cards)


@api_bp.route("/api/cards/<int:id>", methods=["GET"])
def card(id):
    """View a specific card with it's price history

    Args:
         id: ID of card to display

    Returns:
        A json object with the recent card prices
    """
    card = Card.query.filter_by(id=id).first()
    return jsonify(card)
