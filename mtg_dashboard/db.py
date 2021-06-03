from mtg_dashboard.models import db
from flask import Blueprint

db_bp = Blueprint('database', __name__)


@db_bp.cli.command("drop")
def drop():
    """Drop all database tables"""
    db.drop_all()


@db_bp.cli.command("init")
def init():
    """Drop all database tables"""
    db.create_all()
