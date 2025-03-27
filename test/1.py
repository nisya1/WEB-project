from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def to_movies():
    return render_template("{{ url_for(t1.html)}}")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
