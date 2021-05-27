from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
db = SQLAlchemy(app)

collections = db.Table(
    "collections",
    db.Column(
        "collection_id", db.Integer, db.ForeignKey("collection.id"), primary_key=True
    ),
    db.Column("card_id", db.Integer, db.ForeignKey("card.id"), primary_key=True),
)


class Collection:
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


class Card(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    setname = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        return f"{self.name} ({self.setname})"


class Price(db.model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    card_id = db.Column(db.Integer, db.ForeignKey("card.id"), nullable=False)
    card = db.relationship("Card", backref=db.backref("prices", lazy=True))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __repr__(self):
        return f"{self.date}: {self.card.name} {self.price} "