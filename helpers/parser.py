import json

from data_api.cast_dao import get_cast, add_cast
from data_api.movies_dao import movie_exists, add_movie_to_db
from data_api.genre_dao import get_genre, add_genre, attach_movie_to_genre_db

from helpers.logger import LOG
from helpers.db import terminating_sn


class Parser(object):
    def __init__(self, file_location):
        self.file_location = file_location

    def load_file(self):
        file = open(self.file_location)
        data = json.load(file)
        return data

    @staticmethod
    def get_movie_detail(movie):
        popularity = movie['99popularity']
        director = movie['director'].strip()
        genre_list = movie['genre']
        imdb_score = movie['imdb_score']
        name = movie['name'].strip()

        for index, value in enumerate(genre_list):
            # Removing unnecessary spaces
            genre_list[index] = value.strip()

        return popularity, director, genre_list, imdb_score, name

    def attach_movie_to_genre(self, session, movie_id, genre_name):
        genre_obj = get_genre(session, genre_name)
        LOG.info("Checking if genre {} exists in db".format(genre_name))
        if not genre_obj:
            LOG.info("Genre {} doesn't exist, Hence writting".format(genre_name))
            # genre not found, create it.
            genre_obj = add_genre(session, genre_name)
            session.flush()

        attach_movie_to_genre_db(session, movie_id, genre_obj.id)
        LOG.info("Attached genre {} to movie {} ".format(genre_name, movie_id))

    def add_movie(self, session, popularity, director, genre_list, imdb_score, name):
        LOG.info("Checking if director {} exists in db".format(director))
        director_obj = get_cast(session, director)
        if not director_obj:
            LOG.info("Director {} doesn't exist in db hence writting".format(director))
            # director not found in db create it
            director_obj = add_cast(session, director)
            session.flush()
            LOG.info("Director {} written to DB with id as {}".format(director_obj.name, director_obj.id))

        movie_obj = add_movie_to_db(session, popularity, director_obj.id, imdb_score, name)
        session.flush()
        LOG.info("Writting movie to db with id as {}".format(movie_obj.id))

        for genre in genre_list:
            self.attach_movie_to_genre(session, movie_obj.id, genre)

    def populate(self):
        LOG.info("Populating tables")
        loaded_json = self.load_file()
        LOG.info("Json loaded from file {}".format(self.file_location))

        for movie in loaded_json:
            popularity, director, genre_list, imdb_score, name = Parser.get_movie_detail(movie)
            LOG.info("Movie {} selected for write".format(name))
            try:
                with terminating_sn() as session:
                    if not movie_exists(session, name):
                        LOG.info("Movie {} doesn't exists writting".format(name))
                        self.add_movie(session, popularity, director, genre_list, imdb_score, name)
                        session.commit()
                    else:
                        LOG.info("Movie {} exists hence skipping write".format(name))
            except Exception:
                LOG.exception("Exception occured while writting movie {} to db".format(name))
                session.rollback()
