import flask
from flask import render_template

bp = flask.Blueprint("movies", __name__, url_prefix="/movies")


@bp.route("/")
def movies():
    return render_template("movies/index.html")
