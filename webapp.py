import logging
from flask import Flask

from helpers.db import load_db
from helpers.parser import Parser
from views.movies import blueprint


def create_app():
    # Create DB
    # logging.info("Creating DB and binding models")
    # load_db()
    #
    # parser = Parser('imdb.json')
    # parser.populate()

    # Create Table

    # Run Migrations

    # Instantiate flask app
    app = Flask(__name__)

    # Register Blueprint
    app.register_blueprint(blueprint)

    # Return app
    return app


# if __name__ == "__main__":
#     app = create_app()
#     app.run(debug=True)
