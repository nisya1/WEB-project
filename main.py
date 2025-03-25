import blueprints.movies
from flask import Flask, redirect
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)

app.register_blueprint(blueprints.movies.bp)


@app.route('/')
def to_movies():
    return redirect('http://127.0.0.1:8080/movies')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
