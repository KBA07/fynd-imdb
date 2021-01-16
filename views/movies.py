"""
This file contains API endpoints which would be exposed to the outer world
"""
import json

from flask import Blueprint, request

from data_api.movies_dao import parse_json, movie_id_exists, \
    movie_exists, add_movie, delete_movie_from_db, edit_movie, get_movie, get_genre_list
from helpers.db import terminating_sn
from helpers.logger import LOG
from helpers.auth import basic_auth
from helpers.response_maker import ResponseMaker

blueprint = Blueprint('movies', __name__)

MAX_LIMIT = 100
DEFAULT_LIMIT = 20
DEFAULT_OFFSET = 0


def validate_get_limit_offset(limit, offset):
    if limit and limit > MAX_LIMIT or limit < 0:
        limit = MAX_LIMIT

    if not offset or offset < 0:
        offset = 0

    return limit, offset


@blueprint.route('/')
def homepage():
    return "Welcome to IMDB API"


@blueprint.route('/v1/movies', methods=['GET'])
def get_movies():
    """
    Request:
    v1/movies?name=test&genre=Adventure&director=Vic&limit=100&offset=0
    :param name: optional
    :param genre: optional
    :param director: optional
    :param limit: optional
    :param offset: optional

    Response:
    :return: 200, SUCCESS for a successful entry
    200 response
    {
    "data" : [{
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
    }..]
    "total" : <int>
    }
    :return: 500, INTERNAL SERVER ERROR for issue on server side
    """
    name = request.args.get('name')
    director = request.args.get('director')
    genre = request.args.get('genre')
    limit = int(request.args.get('limit', DEFAULT_LIMIT))
    offset = int(request.args.get('offset', DEFAULT_OFFSET))

    limit, offset = validate_get_limit_offset(limit, offset)

    with terminating_sn() as session:
        total, resp = get_movie(session, name, director, genre, limit, offset)

        movie_list = []
        for movie in resp:
            movie_id, popularity, director, genre_blob, imdb_score, name = movie
            movie_list.append({'id': movie_id, '99popularity': popularity,
                               'director': director, 'genre': get_genre_list(genre_blob),
                               'imdb_score': imdb_score, 'name': name})

        resp = {'total': total, 'data': movie_list}
        return ResponseMaker(ResponseMaker.RESPONSE_200).return_response(resp)


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
    popularity = director = genre_list = imdb_score = name = None
    data = json.loads(request.data)

    if data:
        popularity, director, genre_list, imdb_score, name = parse_json(data)

    # Add a validation for popularity and imdb_score

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
    """
    Request:
    v1/movies?id=1
    :param id: Required

    Request Body: - Any one of the field given below is required
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
    :return: 200, SUCCESS for a successful edition
    :return: 400, BAD REQUEST for issue in client request side
    :return: 401, UNAUTHORIZED for wrong user access
    :return: 500, INTERNAL SERVER ERROR for issue on server side
    """
    movie_id = int(request.args.get('id', 0))

    popularity = director = genre_list = imdb_score = name = None
    data = json.loads(request.data)
    if data:
        popularity, director, genre_list, imdb_score, name = parse_json(data)

    # Add a validation for popularity and imdb_score

    if not movie_id or not any([popularity, director, genre_list, imdb_score, name]):
        return ResponseMaker(ResponseMaker.RESPONSE_400, ResponseMaker.RESPONSE_400_MESSAGE,
                             ResponseMaker.RESPONSE_400_ERROR_MISSING_FIELDS).return_response()

    try:
        with terminating_sn() as session:
            if not movie_id_exists(session, movie_id):
                return ResponseMaker(ResponseMaker.RESPONSE_400,
                                     ResponseMaker.RESPONSE_400_MESSAGE,
                                     ResponseMaker.RESPONSE_400_ERROR_ENTRY_MISSING
                                     ).return_response()

            edit_movie(session, movie_id, popularity, director, genre_list, imdb_score, name)
            return ResponseMaker(ResponseMaker.RESPONSE_200).return_response(
                ResponseMaker.RESPONSE_200_MESSAGE)
    except Exception:
        session.rollback()
        LOG.exception("Exception occurred while editing a movie if {} info".format(movie_id))


@blueprint.route('/v1/movies', methods=['DELETE'])
@basic_auth
def delete_movies():
    """
    Request:
    v1/movies?id=1
    :param id: Required

    Response:
    :return: 200, SUCCESS for a successful deletion
    :return: 400, BAD REQUEST for issue in client request side
    :return: 401, UNAUTHORIZED for wrong user access
    :return: 500, INTERNAL SERVER ERROR for issue on server side
    """
    movie_id = int(request.args.get('id', 0))

    if not movie_id:
        return ResponseMaker(ResponseMaker.RESPONSE_400, ResponseMaker.RESPONSE_400_MESSAGE,
                             ResponseMaker.RESPONSE_400_ERROR_MISSING_FIELDS).return_response()

    try:
        with terminating_sn() as session:
            delete_movie_from_db(session, movie_id)

            return ResponseMaker(ResponseMaker.RESPONSE_200).return_response(
                ResponseMaker.RESPONSE_200_MESSAGE)

    except Exception:
        session.rollback()
        LOG.exception("Exception occurred while deleting movie id {} from db".format(movie_id))
        return ResponseMaker(ResponseMaker.RESPONSE_500).return_response(
            ResponseMaker.RESPONSE_500_MESSAGE)
