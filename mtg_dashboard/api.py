from statistics import mean
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
    order_by: sort by different metrics. Accepted values:
        value: sort by current price
        trending: sort by value gained during the last 10 days
    limit: only display <limit> entries

    Returns:
        A json list of all cards in database
    """
    cards = list(Card.query.all())
    order_by = request.args.get("order_by")
    if order_by == "value":
        cards = sorted(cards, key=lambda x: x.current_price if x.current_price else 0, reverse=True)
    if order_by == "trending":
        cards = [[c, calculate_trend(c)] for c in cards]
        cards = sorted(cards, key=lambda x: x[1], reverse=True)

    limit = request.args.get("limit")
    print(limit)
    cards = cards[: int(limit)] if limit else cards

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


@api_bp.route("/api/stats", methods=["GET"])
def stats():
    """List various stats

    Returns:
        A json list of tuples of various stats
    """
    collections = Collection.query.all()

    # we calculate the value with python instead of a query because
    # the query doesn't really work correctly
    avg_value = int((sum([c.value for c in collections]) / len(collections)))

    # here it's important that we exclude null values (with the where clause)
    # because for some reason there are cards with no current price
    max_card_value = (
        Card.query.where(Card.current_price > 0)
        .order_by(Card.current_price.desc())
        .first()
        .current_price
    )

    stats = [
        {"title": "Number of cards", "number": len(Card.query.all())},
        {"title": "Number of collections", "number": len(Collection.query.all())},
        {"title": "Average collection value", "number": f"{avg_value}$"},
        {"title": "Max card value", "number": f"{max_card_value}$"},
    ]

    return jsonify(stats)


def calculate_trend(card):
    """Calculate trend over the last 10 periods

    Args:
        card (Card): Card object

    Return:
        trend (float) Avg Trend for the last 10 periods
    """
    trends = []
    current_price = card.current_price
    try:
        prices = card.prices[1:100]
    except IndexError:
        prices = card.prices

    for price in prices:
        try:
            trend = (current_price - price.price) / price.price
            trends.append(trend)
        except TypeError:
            trends.append(0)
    if not trends:
        return 0
    return mean(trends)
