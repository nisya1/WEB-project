import blueprints.movies, blueprints.auth, blueprints.admin_page, blueprints.map
from api.auth.profile import UserProfileApi
from api.movies.movies import AllMoviesApi
from api.map.map import MapInfoApi
from api.movies.admin import DeleteMovie
from random import choice
from flask import Flask, redirect, session, render_template
from flask_restful import Api


app = Flask(__name__)
app.secret_key = choice(["1", '2', '3'])

app.register_blueprint(blueprints.movies.bp)
app.register_blueprint(blueprints.auth.bp)
app.register_blueprint(blueprints.admin_page.bp)
app.register_blueprint(blueprints.map.bp)

api = Api(app)
api.add_resource(UserProfileApi, '/api/profile/<user_name>')
api.add_resource(AllMoviesApi, '/api/movies/all')
api.add_resource(DeleteMovie, '/api/movies/delete')
api.add_resource(MapInfoApi, '/api/map/cinema')


@app.route('/')
def to_movies():
    return redirect('movies')


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/error404.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
