from datetime import datetime
from dataclasses import dataclass
from typing import List
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


collections = db.Table(
    "collection_card_rel",
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collection.id"), primary_key=True
    ),
    db.Column("card_id", db.Integer, db.ForeignKey("card.id"), primary_key=True),
)


@dataclass
class Card(db.Model):
    id: int
    name: str
    setname: str
    count: int
    img: str
    prices = List["Price"]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(80), nullable=False)
    setname = db.Column(db.String(5), nullable=True)
    count = db.Column(db.Integer, nullable=False, default=1)

    def get_current_price(self):
        return self.prices[0]

    def serialize(self):
        """Returns a dictionary with
        additional information not saved in database"""
        dct = dict()
        dct["id"] = self.id
        dct["name"] = self.name
        dct["setname"] = self.setname
        dct["current_price"] = self.get_current_price()
        dct["count"] = self.count
        dct["img"] = self.img
        return dct

    def __repr__(self):
        if self.setname:
            return f"{self.count}x {self.name} ({self.setname})"
        return f"{self.name}"


@dataclass
class Collection(db.Model):
    id: int
    name: str
    cards = List["Card"]

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    cards = db.relationship(
        "Card",
        secondary=collections,
        lazy="subquery",
        backref=db.backref("collections", lazy=True),
    )

    def serialize(self):
        """Returns a dictionary with
        additional information not saved in database"""
        dct = dict()
        dct["cards"] = self.cards
        dct["number of cards"] = len(self.cards)
        dct["name"] = self.name
        dct["id"] = self.id
        return dct

    def __repr__(self):
        return f"Collection {self.name} ({len(self.cards)} cards)"


@dataclass
class Price(db.Model):
    id: int
    price: float
    card_id: int
    date: datetime

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Float)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    card = db.relationship(
        "Card",
        backref=db.backref("prices", lazy=True, order_by="Price.date.asc()"),
    )
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"Price: {self.date}: {self.card.name} {self.price} "
