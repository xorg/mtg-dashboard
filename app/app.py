import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)


# a simple page that says hello
@app.route("/hello")
def hello():
    env_var = os.environ.get("TEST_VAR")
    return f"Testing env vars: {env_var}"


if __name__ == '__main__':
    app.run()
