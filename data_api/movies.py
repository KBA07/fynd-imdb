from data_api.models import Movies


def movie_exists(session, name):
    return bool(session.query(Movies.id).filter(Movies.name == name).first())


def add_movie_to_db(session, popularity, director_id, imdb_score, name):
    movie = Movies(popularity, director_id, imdb_score, name)
    session.add(movie)
    return movie
