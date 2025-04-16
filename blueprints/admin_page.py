import flask
from flask import render_template, session, abort, request, redirect, url_for
from data.db_session import global_init, create_session
from data.posters_models.events import Events
from data.posters_models.eventgenre import EventGenre
from datetime import datetime

bp = flask.Blueprint("admin_page", __name__, url_prefix="/admin_page")


@bp.route("/", methods=["GET"])
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


@bp.route("/add_film", methods=['POST'])
def add_films():
    global_init(f"database/posters.db")
    sess = create_session()

    name = request.form.get("title")
    genre = request.form.get("genre")
    rating = request.form.get("rating")
    duration = request.form.get("duration")
    session_date = request.form.get("session_date")
    session_date = datetime.strptime(session_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    session_time = request.form.get("session_time")
    price = request.form.get("price")
    image = request.form.get("image")

    movie = Events(
        Title=name,
        GenreId=2,
        Rating=rating,
        Duration=duration,
        ImageName="asdasa",
        Seats=15,
        Price=price,
        Time=f"{session_date} {session_time}"
    )

    sess.add(movie)
    sess.commit()
    return redirect(url_for('to_movies'))


@bp.route("/delete_film", methods=['POST'])
def delete_films():
    id = request.form.get("delete_movie_id")

    global_init(f"database/posters.db")
    sess = create_session()

    film = sess.query(Events).filter(Events.EventId == id).first()

    sess.delete(film)
    sess.commit()

    return redirect(url_for('to_movies'))
