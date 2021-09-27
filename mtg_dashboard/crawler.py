import time
import csv
import scrython
import click
from flask import Blueprint, current_app
from mtg_dashboard.models import Card, Collection, Price, db

crawler_bp = Blueprint("crawler", __name__)


def read_file(filename):
    with open(filename, "r") as f:
        data = f.readlines()
    return data


def parse_decklist_line(line, collection=None):
    """Parse single decklist line
    """
    line = line.strip()
    # if the last character is a closing parenthese, it's the setname
    setname = None
    if line and line[-1] == ")":
        setname = line.split(" ")[-1].strip("()")
        line = " ".join(line.split(" ")[:-1])
    count = int(line.split(" ")[0])
    name = " ".join(line.split(" ")[1:])
    existing_card = Card.query.filter_by(name=name).first()
    if existing_card:
        existing_card.count = int(existing_card.count) + int(count)
        return existing_card
    final_card = Card(name=name, count=count, setname=setname)
    final_card.collections.append(collection)
    return final_card


def parse_csv(filename, collection=None):
    """Parse csv file

    Args:
        filename (str): Path to csv file
        collection (Collection, optional): Collection to add cards to. Defaults to None.

    Returns:
        List[Card]: List of card objects, ready to be saved to database
    """
    cards = []
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row["Name"]
            setname = row["Set"]
            existing_card = Card.query.filter_by(name=name, setname=setname).first()
            if existing_card:
                existing_card.count += 1
                cards.append(existing_card)
                continue
            final_card = Card(name=name, count=1, setname=setname)
            final_card.collections.append(collection)
            cards.append(final_card)
    return cards


def parse_txt(filename, collection=None):
    """Parse txt file

    Args:
        filename (str): Path to txt file
        collection (Collection, optional): Collection to add cards to. Defaults to None.

    Returns:
        List[Card]: List of card objects, ready to be saved to database
    """
    f = read_file(filename)
    return parse_mtg_decklist(f, collection)


def parse_mtg_decklist(data, col=None):
    return [parse_decklist_line(i, col) for i in data if i]


def fetch_price(card):
    """Connect to Scryfall API and download card data"""

    current_app.logger.info(f"Fetching price for {card.name}")
    try:
        if card.setname:
            fetched_card = scrython.cards.Named(exact=card.name, set=card.setname)
        else:
            fetched_card = scrython.cards.Named(exact=card.name)
        if not card.img:
            card.img = fetched_card.image_uris()["normal"]
            save_to_db([card])
        price = Price(card=card, card_id=card.id, price=fetched_card.prices("eur"))
    except scrython.ScryfallError:
        price = None
    # time.sleep(0.05)
    return price


def fetch_prices(card_list):
    """Iterate over list of cards and fetch prices.
    Filter out all null values.
    """
    prices = [fetch_price(card) for card in card_list if card.name]
    return [price for price in prices if price]


def parse_collection(filename, collection):
    """Parse collection filename or instance

    To ensure that it's possible to add new cards
    to the same collection, we try to find out if
    the provided filename corresponds to a database entry.
    If yes, use that collection to add cards to.
    If not, create a new collection.

    """
    # try to find collection
    col = Collection(name=filename.split(".")[0].capitalize())
    if collection:
        col = Collection(name=collection)
        try:
            col_query = col.query.filter_by(name=collection).first()
        except AttributeError:
            col_query = None
        if col_query:
            col = col_query
            return col
    save_to_db([col])
    return col


def save_to_db(objects):
    """Save multiple objects to db. We first create database
    tables to ensure the saving doesn't fail."""
    db.create_all()
    for i in objects:
        current_app.logger.info(f"Saving {i} to database")

        db.session.add(i)
    db.session.commit()


@crawler_bp.cli.command("import")
@click.argument("filename")
@click.option("--collection", default=None, help="Collection name to save cards to")
def import_cards(filename, collection):
    """Import cards to database from either a .txt or .csv file"""

    col = parse_collection(filename, collection)

    extension = filename.split(".")[-1]
    cards = []
    if extension == "csv":
        cards = parse_csv(filename, col)
    else:
        cards = parse_txt(filename, col)

    save_to_db(cards)
    prices = fetch_prices(cards)
    save_to_db(prices)


@crawler_bp.cli.command("update")
@click.option("--dry-run", "-d", default=False, is_flag=True)
def update_prices(dry_run=False):
    """Fetch live prices of all cards save them to database"""
    cards = Card.query.all()
    prices = fetch_prices(cards)
    if dry_run:
        current_app.logger.info(prices)
        return
    save_to_db(prices)


@crawler_bp.cli.command("fetch_images")
def fetch_images(dry_run=False, resolution="normal"):
    """Get image url for every card and save it to db"""
    cards = Card.query.all()
    for card in cards:
        current_app.logger.info(f"Fetching card img for {card.name}...")
        if card.setname:
            fetched_card = scrython.cards.Named(exact=card.name, set=card.setname)
        else:
            fetched_card = scrython.cards.Named(exact=card.name)
        card.img = fetched_card.image_uris()[resolution]
        time.sleep(0.05)
    save_to_db(cards)


if __name__ == "__main__":
    import_cards()
