import blueprints.movies, blueprints.auth, blueprints.admin_page
from random import choice
from flask import Flask, redirect, session, render_template

app = Flask(__name__)
app.secret_key = choice(["1", '2', '3'])

app.register_blueprint(blueprints.movies.bp)
app.register_blueprint(blueprints.auth.bp)
app.register_blueprint(blueprints.admin_page.bp)


@app.route('/')
def to_movies():
    return redirect('movies')


@app.errorhandler(404)
def not_found(error):
    return render_template('errors/error404.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
