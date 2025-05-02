import flask
from flask import render_template, request, session, redirect, flash
from datetime import date
from data.db_session import global_init, create_session
from data.posters_models.events import Events
from data.posters_models.eventgenre import EventGenre
from data.users_models.users import Users


def function(time: str):
    time = tuple(map(int, time.split()[0].split('.')[::-1]))
    return time



bp = flask.Blueprint("movies", __name__, url_prefix="/movies")


@bp.route("/", methods=['GET', 'POST'])
def movies():
    today = date.today()
    search = None
    if request.method == 'POST':
        search = request.form['search_films']
        
    session['user_active'] = session.get('user_active', False)
    session['show_modal'] = session.get('show_modal', False)
    session['base_url'] = request.base_url

    global_init(f"database/posters.db")
    sess = create_session()
    events = [event for event in sess.query(Events).all() if date(*function(event.Time)) > today]
    genres = sess.query(EventGenre).all()

    if search:
        events = [event for event in events if search.lower() in event.Title.lower()]

    params = {
        "events": events,
        "genres": genres,
        "user_active": session['user_active'],
        "show_modal": session['show_modal']
    }

    return render_template("movies/index.html", **params)


@bp.route("/soon", methods=['GET', 'POST'])
def soon_movies():
    today = date.today()
    search = None
    if request.method == 'POST':
        search = request.form['search_films']

    session['user_active'] = session.get('user_active', False)
    session['show_modal'] = session.get('show_modal', False)
    session['base_url'] = request.base_url

    global_init(f"database/posters.db")
    sess = create_session()
    events = [event for event in sess.query(Events).all() if date(*function(event.Time)) > today]
    genres = sess.query(EventGenre).all()

    events.sort(key=lambda x: date(*function(x.Time)))

    if search:
        events = [event for event in events if search.lower() in event.Title.lower()]
    params = {
        "events": events,
        "genres": genres,
        "user_active": session['user_active'],
        "show_modal": session['show_modal']
    }

    return render_template("movies/soon.html", **params)



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

        if ',' not in event.Tickets:
            tickets = tuple()
        else:
            tickets = tuple(map(int, event.Tickets.split(',')))

        params = {
            'event': event,
            'genre': genre,
            'user_active': session['user_active'],
            'show_modal': session['show_modal'],
            'tickets': tickets
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
            seats = event.Tickets.split(',')

            for seat in booked_seats.split(','):
                seats.remove(seat)
            seats = ','.join(seats)

            event.Tickets = seats
            sess.commit()

            global_init(f"database/users.db")
            sess1 = create_session()
            user = sess1.query(Users).filter(Users.Name == session['name']).first()
            tickets = user.Tickets

            if tickets:
                tickets += f'{event.EventId}:{booked_seats};'
            else:
                tickets = f'{event.EventId}:{booked_seats};'

            user.Tickets = tickets
            sess1.commit()
            sess1.expunge_all()
            sess.close()

            print(event, booked_seats)
            return redirect(session['base_url'])
        else:
            flash('Войдите в аккаунт')
    return redirect(session['base_url'])