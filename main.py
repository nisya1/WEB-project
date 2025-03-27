import blueprints.movies, blueprints.auth
from flask import Flask, redirect


app = Flask(__name__)

app.register_blueprint(blueprints.movies.bp)
app.register_blueprint(blueprints.auth.bp)


@app.route('/')
def to_movies():
    return redirect('movies')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
