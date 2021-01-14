from flask import Flask

from views.movies import blueprint


def create_app():
    # Create DB

    # Create Table

    # Run Migrations

    # Instantiate flask app
    app = Flask(__name__)

    # Register Blueprint
    app.register_blueprint(blueprint)

    # Return app
    return app
