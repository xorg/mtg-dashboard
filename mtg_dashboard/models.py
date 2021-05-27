from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config.from_pyfile("config.py")
db = SQLAlchemy(app)

collections = db.Table(
    "collection_card_rel",
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collection.id"), primary_key=True
    ),
    db.Column("card_id", db.Integer, db.ForeignKey("card.id"), primary_key=True),
)


class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    cards = db.relationship(
        "Card",
        secondary=collections,
        lazy="subquery",
        backref=db.backref("collections", lazy=True),
    )

    def __repr__(self):
        return f"Collection {self.name} ({len(self.cards)} cards)"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    setname = db.Column(db.String(5), nullable=True)
    count = db.Column(db.Integer, nullable=False, default=1)

    def __repr__(self):
        return f"{self.name} ({self.setname})"


class Price(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    card = db.relationship("Card", backref=db.backref("prices", lazy=True))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.date}: {self.card.name} {self.price} "
