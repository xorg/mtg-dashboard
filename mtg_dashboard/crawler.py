import scrython
import click
from flask import Blueprint
from mtg_dashboard.models import Card, Price, db

crawler_bp = Blueprint('crawler', __name__)


def read_file(filename):
    with open(filename, "r") as f:
        data = f.readlines()
    return data


def parse_decklist_line(line):
    line = line.strip()
    # if the last line is a bracket, it's the setname
    setname = None
    if line and line[-1] == ")":
        setname = line.split(" ")[-1].strip("()")
        line = " ".join(line.split(" ")[:-1])
    count = line.split(" ")[0]
    name = " ".join(line.split(" ")[1:])
    return Card(name=name, count=count, setname=setname)


def parse_mtg_decklist(data):
    return [parse_decklist_line(i) for i in data if i]


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
        crawler_bp.logger.info(f"Importing {i}")

        db.session.add(i)
    db.session.commit()


@crawler_bp.cli.command("import")
@click.argument("filename")
def import_cards(filename):
    """Import cards to database from a text file"""
    f = read_file(filename)
    cards = parse_mtg_decklist(f)
    save_to_db(cards)
    prices = fetch_prices(cards)
    save_to_db(prices)


if __name__ == "__main__":
    import_cards()
