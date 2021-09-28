import itertools
from datetime import datetime
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import select, func
from typing import List


db = SQLAlchemy()


collections = db.Table(
    "collection_card_rel",
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collection.id"), primary_key=True
    ),
    db.Column("card_id", db.Integer, db.ForeignKey("card.id"), primary_key=True),
)


@dataclass
class Price(db.Model):
    """Price of a card at a given point in time"""

    id: int
    price: float
    card_id: int
    date: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    card = db.relationship(
        "Card",
        backref=db.backref("prices", lazy=True, order_by="Price.date.desc()"),
    )
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Price: {self.date}: {self.card.name} {self.price} "


@dataclass
class Card(db.Model):
    "Representation of a single card"
    current_price: float
    id: int
    name: str
    setname: str
    count: int
    img: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(80), nullable=False)
    setname = db.Column(db.String(5), nullable=True)
    count = db.Column(db.Integer, nullable=False, default=1)

    @hybrid_property
    def current_price(self):
        """Show most recent price of this card
        Prices are sorted by default by date, we
        don't have to do any sorting here.
        """
        if self.prices:
            return self.prices[0].price
        return None

    @current_price.expression
    def current_price(cls):
        return (
            select([Price.price])
            .where(Price.card_id == cls.id)
            .limit(1)
            .scalar_subquery()
        )

    def __repr__(self):
        if self.setname:
            return f"{self.count}x {self.name} ({self.setname})"
        return f"{self.name}"


@dataclass
class Collection(db.Model):
    "Collection of cards"
    value_history: List
    value: float
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    cards = db.relationship(
        "Card",
        secondary=collections,
        lazy="dynamic",
        backref=db.backref("collections", lazy=True),
    )

    @hybrid_property
    def value(self):
        """This method calculates the current value of this collection
        The hybrid_property allows usage of Card.current_value just like
        a regular database column.
        """
        return sum([c.current_price for c in self.cards if c.current_price])

    @value.expression
    def value(cls):
        "Query expression to calculate collection value"
        return select(func.sum(Card.current_price)).join(cls.cards)

    @hybrid_property
    def value_history(self):
        """This method calculates the total value of the collection
        for each point in time recorded by all the price objects
        in all card objects that are contained in the collection
        """
        prices = list(
            itertools.chain.from_iterable([card.prices for card in self.cards])
        )
        s = sorted(prices, key=lambda x: x.date.date())
        plist = []

        # output data as an array of x and y for easy displaying
        # with ApexChart, the frontend charting library
        for key, group in itertools.groupby(s, lambda x: x.date.date()):
            plist.append(
                {
                    "x": key.strftime("%Y-%m-%d"),
                    "y": sum([int(p.price or 0) for p in group]),
                }
            )

        return [{"data": plist}]

    @value_history.expression
    def value_history(cls):
        """Query expression to calculate value history"""
        subquery = select(Price.id).join(Card, Card.collection_id == cls.id)
        return (
            select(func.sum(Price.price), Price.date)
            .where(Price.id.in_(subquery))
            .order_by(Price.date.desc())
            .group_by(Price.date)
        )

    def __repr__(self):
        return f"Collection {self.name}"
