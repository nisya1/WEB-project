from flask import render_template
from data.db_session import global_init, create_session
from data.posters_models.events import Events


def main_page():
    global_init(f"database/posters.db")
    sess = create_session()
    events = sess.query(Events).all()



    return render_template("movies/index.html", events=events)