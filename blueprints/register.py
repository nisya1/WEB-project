import flask
from flask import render_template, request
from data.db_session import global_init, create_session
from data.posters_models.events import Events

bp = flask.Blueprint("register", __name__, url_prefix="/register")


@bp.route('/', methods=['GET'])
def register():
    return render_template('register/register.html')