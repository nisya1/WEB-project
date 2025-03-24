from flask import Flask

import blueprints.movies

app = Flask(__name__)

app.register_blueprint(blueprints.movies.bp)

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
