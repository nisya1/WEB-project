import flask
import os
from flask import render_template, session, abort, request, redirect, url_for
from data.db_session import global_init, create_session
from data.posters_models.events import Events
from data.posters_models.eventgenre import EventGenre
from datetime import datetime
from werkzeug.utils import secure_filename
from uuid import uuid4

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
        'user_active': session['user_active'],
        "movies": movies,
        "genres": genres,
    }

    return render_template("admin/ad.html", **params)


@bp.route("/add_film", methods=['POST'])
def add_films():
    global_init(f"database/posters.db")
    sess = create_session()

    name = request.form.get("title")
    genre_name = request.form.get("genre")
    rating = request.form.get("rating")
    duration = request.form.get("duration")
    session_date = request.form.get("session_date")
    session_date = datetime.strptime(session_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    session_time = request.form.get("session_time")
    price = request.form.get("price")
    image = request.files["image"]
    genre = sess.query(EventGenre).filter(EventGenre.GenreName == genre_name).first()

    upload_folder = os.path.join('static', 'movies', 'images')
    os.makedirs(upload_folder, exist_ok=True)
    filename = f"{uuid4()}_{secure_filename(image.filename)}"
    filepath = os.path.join(upload_folder, filename)
    image.save(filepath)

    movie = Events(
        Title=name,
        GenreId=genre.GenreId,
        Rating=rating,
        Duration=duration,
        ImageName=filename,
        Seats=15,
        Price=price,
        Time=f"{session_date} {session_time}",
        Tickets="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15"
    )

    sess.add(movie)
    sess.commit()
    return redirect(url_for('to_movies'))


@bp.route("/delete_film", methods=['POST'])
def delete_films():
    id = request.form.get("delete_movie_id")
    try:
        image_name = request.form.get("delete_image_name")

        upload_folder = os.path.join('static', 'movies', 'images')
        filepath = os.path.join(upload_folder, image_name)
        os.remove(filepath)
    except:
        pass

    global_init(f"database/posters.db")
    sess = create_session()

    film = sess.query(Events).filter(Events.EventId == id).first()

    sess.delete(film)
    sess.commit()

    return redirect(url_for('to_movies'))


@bp.route("/change_films", methods=['POST'])
def change_films():
    global_init(f"database/posters.db")
    sess = create_session()

    movie_id = request.form.get("movie_id")
    old_image_name = request.form.get("old_image")

    name = request.form.get("title")
    genre_name = request.form.get("genre")
    genre = sess.query(EventGenre).filter(EventGenre.GenreName == genre_name).first().GenreId

    rating = request.form.get("rating")
    duration = request.form.get("duration")

    session_date = request.form.get("session_date")
    session_date = datetime.strptime(session_date, "%Y-%m-%d").strftime("%d.%m.%Y")
    session_time = request.form.get("session_time")

    price = request.form.get("price")
    image = request.files["image"]

    movie = sess.query(Events).filter(Events.EventId == movie_id).first()


    movie.Title = name
    movie.GenreId = genre
    movie.Rating = rating
    movie.Duration = duration
    movie.Time = f"{session_date} {session_time}"
    movie.Price = price

    if image:
        try:
            upload_folder = os.path.join('static', 'movies', 'images')
            filepath = os.path.join(upload_folder, old_image_name)
            os.remove(filepath)
        except:
            pass

        upload_folder = os.path.join('static', 'movies', 'images')
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"{uuid4()}_{secure_filename(image.filename)}"
        filepath = os.path.join(upload_folder, filename)
        image.save(filepath)

        movie.ImageName = filename

    sess.commit()

    return redirect(url_for('to_movies'))
