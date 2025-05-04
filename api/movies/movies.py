from flask import jsonify, session, make_response
from flask_restful import Resource, abort

from data.db_session import global_init, create_session
from data.posters_models.events import Events
from data.posters_models.eventgenre import EventGenre


class AllMoviesApi(Resource):
    def get(self):
        global_init(f"database/posters.db")
        sess = create_session()
        movies = sess.query(Events).all()
        genres = sess.query(EventGenre).all()
        output = {}

        for movie in movies:
            cur_data = {}
            cur_data['genre'] = str(genres[movie.GenreId - 1])
            cur_data['rating'] = movie.Rating
            cur_data['duration'] = movie.Duration
            cur_data['price'] = movie.Price
            cur_data['time'] = movie.Time
            cur_data['tickets'] = movie.Tickets
            cur_data['seats'] = movie.Seats

            output[movie.Title] = cur_data

        return jsonify({"movies": output})
