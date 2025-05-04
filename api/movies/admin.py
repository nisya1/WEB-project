import os
from flask import jsonify, session, make_response, request
from flask_restful import Resource, abort
from bcrypt import checkpw

from data.db_session import global_init, create_session
from data.users_models.users import Users
from data.posters_models.events import Events



class DeleteMovie(Resource):
    def delete(self):
        if not request.json:
            return make_response(jsonify({'error': 'Empty request'}), 400)
        elif not all(key in request.json for key in
                     ['admin_email', 'admin_password', 'movie_id']):
            return make_response(jsonify({'error': 'Bad request'}), 400)

        email = request.json['admin_email']
        password = request.json['admin_password']

        global_init(f"database/users.db")
        sess1 = create_session()
        user = sess1.query(Users).filter(Users.Email == email).first()

        if user:
            if checkpw(bytes(password, 'UTF8'), bytes(user.Password, 'UTF8')):
                if user.RoleId == 1:
                    movie_id = request.json['movie_id']

                    global_init(f"database/posters.db")
                    sess = create_session()

                    film = sess.query(Events).filter(Events.EventId == movie_id).first()

                    if film:
                        try:
                            image_name = film.ImageName
                            upload_folder = os.path.join('static', 'movies', 'images')
                            filepath = os.path.join(upload_folder, image_name)
                            os.remove(filepath)
                        except:
                            pass

                        sess.delete(film)
                        sess.commit()

                        return make_response(jsonify({'Answer': 'Film deleted'}), 200)
                    return make_response(jsonify({'error': 'Film does not exist'}), 404)

        return make_response(jsonify({'error': 'Access denied'}), 403)
