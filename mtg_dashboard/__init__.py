import os
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    # Configure CORS to make frontend work
    CORS(app)
    env = os.environ.get("FLASK_ENV")
    app.config.from_object(f'mtg_dashboard.config.{env.capitalize()}')
    
    # 
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from .models import db
    db.init_app(app)
    Migrate(app, db, render_as_batch=True)


def register_blueprints(app):
    """ Use blueprints
    Blueprints allow our application to be modular"""
    from .crawler import crawler_bp
    from .api import api_bp

    app.register_blueprint(crawler_bp)
    app.register_blueprint(api_bp)


app = create_app()
