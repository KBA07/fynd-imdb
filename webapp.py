from flask import Flask

from helpers.db import load_db
from helpers.parser import Parser

from views.movies import blueprint


def register_flask_blueprint(app=None, init_db=False):

    if init_db:
        # Create DB and initialize
        load_db()

        parser = Parser('imdb.json')
        parser.populate()
    
    if not app:
        # Instantiate flask app
        app = Flask(__name__)

    # Register Blueprint
    app.register_blueprint(blueprint, url_prefix='/portfolios/fynd-imdb')

    # Return app
    return app


if __name__ == "__main__":
    app = register_flask_blueprint(None, True)
    app.run(debug=True)
