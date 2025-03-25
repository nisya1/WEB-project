from flask import Flask, redirect

import blueprints.movies

app = Flask(__name__)

@app.route('/')
def to_movies():
    return redirect('http://127.0.0.1:8080/movies')


app.register_blueprint(blueprints.movies.bp)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
