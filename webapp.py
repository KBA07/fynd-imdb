import logging
from flask import Flask

from helpers.db import load_db, terminating_sn
from models.movies import Movies
from views.movies import blueprint


def create_app():
    # Create DB
    logging.info("Creating DB and binding models")
    load_db()

    with terminating_sn() as session:
        movie = Movies(88.8, "Kashif", 7.1,  "haunted")
        session.add(movie)
        session.commit()
        print(session.query(Movies).all())

    # Create Table

    # Run Migrations

    # Instantiate flask app
    app = Flask(__name__)

    # Register Blueprint
    app.register_blueprint(blueprint)

    # Return app
    return app
