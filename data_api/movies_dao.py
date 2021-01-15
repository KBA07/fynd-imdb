from data_api.models import Movies
from data_api.cast_dao import get_cast, add_cast
from data_api.genre_dao import attach_movie_to_genre
from helpers.db import enable_foreign_keys

GENRE_MARKER = '$'


def movie_exists(session, name):
    return bool(session.query(Movies.id).filter(Movies.name == name).first())


def add_movie_to_db(session, popularity, director_id, imdb_score, name, genre_blob):
    movie = Movies(popularity, director_id, imdb_score, name, genre_blob)
    session.add(movie)
    return movie


def add_movie(session, popularity, director, genre_list, imdb_score, name):
    director_obj = get_cast(session, director)
    if not director_obj:
        director_obj = add_cast(session, director)
        session.flush()

    genre_blob = GENRE_MARKER.join(genre for genre in genre_list)
    movie_obj = add_movie_to_db(session, popularity, director_obj.id, imdb_score, name, genre_blob)
    session.flush()

    for genre in genre_list:
        attach_movie_to_genre(session, movie_obj.id, genre)

    session.commit()


def delete_movie_from_db(session, movie_id):
    enable_foreign_keys(session)
    session.query(Movies).filter(Movies.id == movie_id).delete()
    session.commit()


def parse_json(movie_json):
    popularity = movie_json.get('99popularity')
    director = movie_json.get('director').strip()
    genre_list = movie_json.get('genre')
    imdb_score = movie_json.get('imdb_score')
    name = movie_json.get('name').strip()

    for index, value in enumerate(genre_list):
        # Removing unnecessary spaces
        genre_list[index] = value.strip()

    return popularity, director, genre_list, imdb_score, name
