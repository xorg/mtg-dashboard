from flask import Blueprint

views_bp = Blueprint('views', __name__)


# a simple page that says hello
@views_bp.route("/hello")
def hello():
    return "Helllooooo"
