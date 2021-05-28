import scrython
import click
from flask import Blueprint, current_app
from mtg_dashboard.models import Card, Collection, Price, db

crawler_bp = Blueprint('crawler', __name__)


def read_file(filename):
    with open(filename, "r") as f:
        data = f.readlines()
    return data


def parse_decklist_line(line, collection=None):
    line = line.strip()
    # if the last line is a bracket, it's the setname
    setname = None
    if line and line[-1] == ")":
        setname = line.split(" ")[-1].strip("()")
        line = " ".join(line.split(" ")[:-1])
    count = line.split(" ")[0]
    name = " ".join(line.split(" ")[1:])
    existing_card = Card.query.filter_by(name=name).first()
    if existing_card:
        existing_card.count += count
        return existing_card
    final_card = Card(name=name, count=count, setname=setname)
    final_card.collections.append(collection)
    return final_card


def parse_mtg_decklist(data, col=None):
    return [parse_decklist_line(i, col) for i in data if i]


def fetch_price(card):
    if card.setname:
        fetched_card = scrython.cards.Named(exact=card.name, set=card.setname)
    else:
        fetched_card = scrython.cards.Named(exact=card.name)
    price = Price(card=card, card_id=card.id, price=fetched_card.prices("eur"))
    return price


def fetch_prices(card_list):
    return [fetch_price(card) for card in card_list if card.name]


def save_to_db(objects):
    # create db if not exists
    db.create_all()
    for i in objects:
        current_app.logger.info(f"Saving {i} to database")

        db.session.add(i)
    db.session.commit()


@crawler_bp.cli.command("import")
@click.argument("filename")
@click.option('--collection', default=None, help='Collection name to save cards to')
def import_cards(filename, collection):
    """Import cards to database from a text file"""
    f = read_file(filename)

    # try to find collection
    col = Collection(name=filename.split('.')[0].capitalize())
    if collection:
        col = Collection(name=collection)
        try:
            col_query = collection.query.filter_by(name=collection).first()
        except AttributeError:
            col_query = None
        if col_query:
            col = col_query
    save_to_db([col])
    cards = parse_mtg_decklist(f, col)
    save_to_db(cards)
    prices = fetch_prices(cards)
    save_to_db(prices)


@crawler_bp.cli.command("update")
def update_prices():
    """Updates prices of all cards in database"""
    cards = Card.query.all()
    prices = fetch_prices(cards)
    save_to_db(prices)


if __name__ == "__main__":
    import_cards()
