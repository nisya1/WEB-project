import flask
from flask import render_template, session, abort
from data.db_session import global_init, create_session
from data.posters_models.events import Events
from data.posters_models.eventgenre import EventGenre

bp = flask.Blueprint("admin_page", __name__, url_prefix="/admin_page")


@bp.route("/")
def page_open():
    if session["role"] != 1:
        return abort(404)

    global_init(f"database/posters.db")
    sess = create_session()
    movies = sess.query(Events).all()
    genres = sess.query(EventGenre).all()

    params = {
        "movies": movies,
        "genres": genres,
    }

    return render_template("admin/ad.html", **params)
