from datetime import datetime
from dataclasses import dataclass
from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import object_session
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy import select, func


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
        if self.prices:
            return self.prices[0].price
        return None

    @current_price.expression
    def current_price(cls):
        return select([Price.price]).where(Price.card_id == cls.id).limit(1).as_scalar()

    def __repr__(self):
        if self.setname:
            return f"{self.count}x {self.name} ({self.setname})"
        return f"{self.name}"


@dataclass
class Collection(db.Model):
    value: float
    # cards: List["Card"]
    id: int
    name: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    cards = db.relationship(
        "Card",
        secondary=collections,
        lazy="subquery",
        backref=db.backref("collections", lazy=True),
    )

    @hybrid_property
    def value(self):
        return sum([c.current_price for c in self.cards if c.current_price])

    @value.expression
    def value(cls):
        return select(func.sum([Card.current_price])).where(Card.collection_id == cls.id).as_scalar()

    def value_history(self):
        return select(func.sum(Price.price), Price.date).where(Price.card_id == self.id).order_by(Price.date.desc()).group_by(Price.date)

    def __repr__(self):
        return f"Collection {self.name} ({len(self.cards)} cards)"


@event.listens_for(Price, "after_insert")
def receive_after_insert(mapper, connection, price):
    "listen for the 'after_insert' event"
    session = object_session(price)
    card = price.card
    collections = card.collections
    try:
        session.begin_nested()
        for c in collections:
            c.value = c.get_collection_value()
            print(f"{c} current value is {c.value}")
            session.add(c)
            print("Just Updated price for: ", c)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        raise e
