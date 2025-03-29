import flask
from flask import render_template, request, session
from data.db_session import global_init, create_session
from data.posters_models.events import Events


bp = flask.Blueprint("movies", __name__, url_prefix="/movies")


@bp.route("/")
def movies():
    session['user_active'] = session.get('user_active', False)
    session['show_modal'] = session.get('show_modal', False)

    global_init(f"database/posters.db")
    sess = create_session()
    events = sess.query(Events).all()

    params = {
        "events": events,
        "user_active": session['user_active'],
        "show_modal": session['show_modal']
    }

    return render_template("movies/index.html", **params)


@bp.route('/<event_id>', methods=['GET'])
def movie(event_id: int):
    global_init(f"database/posters.db")
    session = create_session()
    event = session.query(Events).filter(Events.EventId == event_id).first()

    if event:
        return render_template('movies/movie.html', event=event)
    return render_template('movies/movie_not_found.html')


@bp.route('/buy_ticket/<event_id>', methods=['POST'])
def buy_ticket(event_id: int):
    pass
