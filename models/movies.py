from sqlalchemy import Column, UniqueConstraint, Index

from sqlalchemy.dialects.sqlite import CHAR, FLOAT

from models.base import Base


class Movies(Base):
    __tablename__ = 'movies'
    id = Column(CHAR(50), primary_key=True, autoincrement=True)
    popularity = Column(FLOAT)
    director = Column(CHAR(50))
    imdb_score = Column(FLOAT)
    name = Column(CHAR(100))

    __table_args__ = (
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
        return "Id={} Popularity={} Director={} Imdb Score={} Name={}".format(
            self.id, self.popularity, self.director, self.imdb_score, self.name)
