import flask
from flask import render_template, request, session
from data.db_session import global_init, create_session
from data.posters_models.events import Events

bp = flask.Blueprint("register", __name__, url_prefix="/register")


@bp.route('/', methods=['GET'])
def register_form():
    return render_template('register/register.html')


@bp.route('/', methods=['POST', "GET"])
def create_account():
    name = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password == confirm_password:
        pass

    return f"{name}, {email}, {password}, {confirm_password}"
