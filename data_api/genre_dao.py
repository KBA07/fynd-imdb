from data_api.models import Genres, MovieGenre


class GenreDao(object):
    @staticmethod
    def get_genre(session, name):
        return session.query(Genres).filter(Genres.name == name).first()

    @staticmethod
    def add_genre(session, name):
        genre = Genres(name)
        session.add(genre)
        return genre

    @staticmethod
    def attach_movie_to_genre_db(session, movie_id, genre_id):
        movie_genre = MovieGenre(movie_id, genre_id)
        session.add(movie_genre)
        return movie_genre

    @staticmethod
    def attach_movie_to_genre(session, movie_id, genre_name):
        genre_obj = GenreDao.get_genre(session, genre_name)
        if not genre_obj:
            # genre not found, create it.
            genre_obj = GenreDao.add_genre(session, genre_name)
            session.flush()

        GenreDao.attach_movie_to_genre_db(session, movie_id, genre_obj.id)

    @staticmethod
    def clear_movie_genre_map(session, movie_id):
        session.query(MovieGenre).filter(MovieGenre.movie_id == movie_id).delete()
