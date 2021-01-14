from sqlalchemy import Column, Index, ForeignKeyConstraint
from sqlalchemy.dialects.sqlite import CHAR, REAL, INTEGER

from models.base import Base


class Movies(Base):
    __tablename__ = 'movies'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    popularity = Column(REAL)
    director_id = Column(INTEGER)
    imdb_score = Column(REAL)
    name = Column(CHAR(100))

    __table_args__ = (
        ForeignKeyConstraint(['director_id'], ['person.id'], name='director_id_fx_key'),
        Index('id_index', 'id'),
        Index('name_index', 'name'),
        Index('director_index', 'director')
    )

    def __init__(self, popularity, director, imdb_score, name):
        self.popularity = popularity
        self.director = director
        self.imdb_score = imdb_score
        self.name = name

    def __repr__(self):
        return "Movies table Id={} Popularity={} Director={} Imdb Score={} Name={}".format(
            self.id, self.popularity, self.director, self.imdb_score, self.name)
