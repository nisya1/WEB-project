import flask
from flask import render_template, request, session, redirect
from data.db_session import global_init, create_session
from data.posters_models.events import Events
from data.posters_models.eventgenre import EventGenre


bp = flask.Blueprint("movies", __name__, url_prefix="/movies")


@bp.route("/", methods=['GET', 'POST'])
def movies():
    search = None
    if request.method == 'POST':
        search = request.form['search_films']
        
    session['user_active'] = session.get('user_active', False)
    session['show_modal'] = session.get('show_modal', False)
    session['base_url'] = request.base_url

    global_init(f"database/posters.db")
    sess = create_session()
    events = sess.query(Events).all()
    genres = sess.query(EventGenre).all()

    if search:
        events = [event for event in events if search.lower() in event.Title.lower()]

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

    params = {
        "events": events,
        "genres": genres,
        "user_active": session['user_active'],
        "show_modal": session['show_modal']
    }

    return render_template("movies/index.html", **params)


@bp.route('/<event_id>', methods=['GET'])
def movie(event_id: int):
    session['user_active'] = session.get('user_active', False)
    session['show_modal'] = session.get('show_modal', False)
    session['base_url'] = request.base_url

    global_init(f"database/posters.db")
    sess = create_session()
    event = sess.query(Events).filter(Events.EventId == event_id).first()

    if event:
        genre = sess.query(EventGenre).filter(EventGenre.GenreId == event.GenreId).first()
        params = {
            'event': event,
            'genre': genre,
            'user_active': session['user_active'],
            'show_modal': session['show_modal'],
            'tickets': tuple(map(int, event.Tickets.split(',')))
        }

        return render_template('movies/movie.html', **params)

    params = {
        'user_active': session['user_active'],
        'show_modal': session['show_modal'],
    }
    return render_template('movies/movie_not_found.html', **params)


@bp.route('/buy_ticket/<event_id>', methods=['POST'])
def buy_ticket(event_id: int):
    booked_seats = request.form['seats']

    if booked_seats != '':
        if session['user_active']:
            sess = create_session()
            event = sess.query(Events).filter(Events.EventId == event_id).first()
            print(event, booked_seats)
    return redirect(session['base_url'])