import os
from flask import Flask


def create_app():
    app = Flask(__name__)
    env = os.environ.get("FLASK_ENV")
    app.config.from_object(f'mtg_dashboard.config.{env.capitalize()}')
    register_extensions(app)
    register_blueprints(app)
    return app


def register_extensions(app):
    from .models import db
    db.init_app(app)


def register_blueprints(app):
    from .crawler import crawler_bp
    from .views import views_bp

    app.register_blueprint(crawler_bp)
    app.register_blueprint(views_bp)


app = create_app()
