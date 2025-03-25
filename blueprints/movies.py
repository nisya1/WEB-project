import flask
from flask import render_template, request
from data.db_session import global_init, create_session
from data.posters_models.events import Events

bp = flask.Blueprint("movies", __name__, url_prefix="/movies")


@bp.route("/")
def movies():
    global_init(f"database/posters.db")
    session = create_session()
    events = session.query(Events).all()



    # new_event = Events(
    #     Title="DANDADAN",
    #     GenreId=1,
    #     TypeId=1,
    #     Rating=9.4,
    #     Duration="10:00",
    #     Image="010001"
    # )
    # session.add(new_event)
    # session.commit()

    return render_template("movies/index.html", events=events,
                           path='../static/movies/images/')


@bp.route('/buy_ticket', methods=['POST'])
def buy_ticket():
    title = request.form.get('movie_title')
    movie_id = request.form.get('movie_id')

    return render_template('movies/movie.html')
