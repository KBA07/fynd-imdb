from data_api.models import Genres, MovieGenre


def get_genre(session, name):
    return session.query(Genres).filter(Genres.name == name).first()


def add_genre(session, name):
    genre = Genres(name)
    session.add(genre)
    return genre


def attach_movie_to_genre_db(session, movie_id, genre_id):
    movie_genre = MovieGenre(movie_id, genre_id)
    session.add(movie_genre)
    return movie_genre


def attach_movie_to_genre(session, movie_id, genre_name):
    genre_obj = get_genre(session, genre_name)
    if not genre_obj:
        # genre not found, create it.
        genre_obj = add_genre(session, genre_name)
        session.flush()

    attach_movie_to_genre_db(session, movie_id, genre_obj.id)
