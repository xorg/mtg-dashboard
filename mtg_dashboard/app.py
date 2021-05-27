import os
import click
from .crawler import fetch_cards
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)


# register cli command
@app.cli.command("fetch")
@click.argument("filename")
def fetch(filename):
    fetch_cards(filename)


app.cli.add_command(fetch)


# a simple page that says hello
@app.route("/hello")
def hello():
    env_var = os.environ.get("TEST_VAR")
    return f"Testing env vars: {env_var}"


if __name__ == '__main__':
    app.run()
