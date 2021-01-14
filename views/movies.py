"""
This file contains API endpoints which would be exposed to the outer world
"""
from flask import Blueprint

blueprint = Blueprint('movies', __name__)


@blueprint.route('/')
def homepage():
    return "Welcome to IMDB API"


@blueprint.route('/v1/movies', methods=['GET'])
def get_movies():
    return "Accessing movies"


@blueprint.route('/v1/movies', methods=['POST'])
def add_movies():
    return "Adding Movies"


@blueprint.route('/v1/movies', methods=['PUT'])
def edit_movies():
    return "Edit Movies"


@blueprint.route('/v1/movies', methods=['DELETE'])
def delete_movies():
    return "Delete Movies"
