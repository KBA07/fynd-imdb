from sqlalchemy import Column, Index, ForeignKeyConstraint
from sqlalchemy.dialects.sqlite import INTEGER, CHAR

from models.base import Base


class Genres(Base):
    __tablename__ = 'genres'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(CHAR(20))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Genre Table Id={}, Name={}".format(self.id, self.name)

    __table_args__ = (
        Index('id_index', 'id'),
        Index('name_index', 'name')
    )


class MovieGenre(Base):
    __tablename__ = 'movie_genre'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    movie_id = Column(INTEGER)
    genre_id = Column(INTEGER)

    __table_args__ = (
        ForeignKeyConstraint(['movie_id'], ['movies.id'], ondelete='CASCADE' ,
                             name='movie_id_fx_key'),
        ForeignKeyConstraint(['genre_id'], ['genres.id'], ondelete='CASCADE',
                             name='genre_id_fx_key'),
        Index('id_index', 'id')
    )

    def __init__(self, movie_id, genre_id):
        self.movie_id = movie_id
        self.genre_id = genre_id

    def __repr__(self):
        return "Movie Genre Table Id={} Movie ID={}, Genre ID={}".format(
            self.id, self.movie_id, self.genre_id)
