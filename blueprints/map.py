import flask
from flask import render_template, request, session, redirect, flash


bp = flask.Blueprint("map", __name__, url_prefix="/map")


@bp.route("/", methods=['GET', 'POST'])
def show_map():
    session['user_active'] = session.get('user_active', False)
    session['base_url'] = request.base_url

    params = {
        "user_active": session['user_active'],
    }

    return render_template("maps/map1.html", **params)
