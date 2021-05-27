import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# load .env file explicitely so that it works in production
# in dev environment the flask dev server loads it automatically
load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)


# a simple page that says hello
@app.route("/hello")
def hello():
    env_var = os.environ.get("TEST_VAR")
    return f"Testing env vars: {env_var}"


if __name__ == '__main__':
    app.run()
