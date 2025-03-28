import flask
from flask import render_template, request, session, redirect, url_for
from data.db_session import global_init, create_session
from data.posters_models.events import Events

bp = flask.Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/register', methods=['GET', 'POST'])
def register_form():
    if request.method == 'POST':
        name = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password == confirm_password:
            session["name"] = name
            session["email"] = email
            session["password"] = password
            session["user_active"] = True

            return redirect(url_for('to_movies'))

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        pass
    return render_template('auth/login.html')
