"""
This file contains API endpoints which would be exposed to the outer world
"""
import json

from flask import Blueprint, request

from data_api.movies_dao import parse_json, movie_exists, add_movie
from helpers.db import terminating_sn
from helpers.logger import LOG
from helpers.auth import basic_auth
from helpers.response_maker import ResponseMaker

blueprint = Blueprint('movies', __name__)


@blueprint.route('/')
def homepage():
    return "Welcome to IMDB API"


@blueprint.route('/v1/movies', methods=['GET'])
def get_movies():
    return "Accessing movies"


@blueprint.route('/v1/movies', methods=['POST'])
@basic_auth
def add_movies():
    """
    Endpoint for adding new movies accepts json input. ALL Fields Mandatory
    Request Body:
    {
    "99popularity": 83.0,
    "director": "Victor Fleming",
    "genre": [
      "Adventure",
      " Family",
      " Fantasy",
      " Musical"
    ],
    "imdb_score": 8.3,
    "name": "The Wizard of Oz"
    }
    Response:
    :return: 200, SUCCESS for a successful entry
    :return: 400, BAD REQUEST for issue in client request side
    :return: 401, UNAUTHORIZED for wrong user access
    :return: 500, INTERNAL SERVER ERROR for issue on server side
    """
    data = json.loads(request.data)
    popularity, director, genre_list, imdb_score, name = parse_json(data)

    if not all([popularity, director, genre_list, imdb_score, name]):
        return ResponseMaker(ResponseMaker.RESPONSE_400, ResponseMaker.RESPONSE_400_MESSAGE,
                             ResponseMaker.RESPONSE_400_ERROR_MISSING_FIELDS).return_response()

    try:
        with terminating_sn() as session:
            if movie_exists(session, name):
                return ResponseMaker(ResponseMaker.RESPONSE_400,
                                     ResponseMaker.RESPONSE_400_MESSAGE,
                                     ResponseMaker.RESPONSE_400_ERROR_ENTRY_PRESENT
                                     ).return_response()

            add_movie(session, popularity, director, genre_list, imdb_score, name)
            return ResponseMaker(ResponseMaker.RESPONSE_200).return_response(
                ResponseMaker.RESPONSE_200_MESSAGE)
    except Exception:
        session.rollback()
        LOG.exception("Exception occurred while writting movie {} to db".format(name))
        return ResponseMaker(ResponseMaker.RESPONSE_500).return_response(
            ResponseMaker.RESPONSE_500_MESSAGE)


@blueprint.route('/v1/movies', methods=['PUT'])
@basic_auth
def edit_movies():
    return "Edit Movies"


@blueprint.route('/v1/movies', methods=['DELETE'])
@basic_auth
def delete_movies():
    """
    v1/movies?id=1
    :return: 200, For delete
    :return: 400, For Ba
    """
    LOG.info(request.args.get('id'))
    return "Delete Movies"
