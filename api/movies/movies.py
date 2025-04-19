from flask import jsonify, session, make_response
from flask_restful import Resource, abort

from data.db_session import global_init, create_session
from data.posters_models.events import Events


class AllMoviesApi(Resource):
    def get(self):
        global_init(f"database/posters.db")
        sess = create_session()
        movies = sess.query(Events).all()
        output = {}

        for movie in movies:
            cur_data = {}
            cur_data['title'] = movie.Title
            cur_data['genre_id'] = movie.GenreId
            cur_data['rating'] = movie.Rating
            cur_data['duration'] = movie.Duration
            cur_data['price'] = movie.Price
            cur_data['time'] = movie.Time

            output[movie.EventId] = cur_data

        return jsonify({"movies": output})
