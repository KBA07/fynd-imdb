from sqlalchemy import Column, Index
from sqlalchemy.dialects.sqlite import CHAR, INTEGER

from models.base import Base


class Persons(Base):
    __tablename__ = 'persons'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(CHAR(50))

    __table_args__ = (
        Index('id_index', 'id'),
        Index('name_index', 'name')
    )

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Persons table Id={}, name={}".format(self.id, self.name)
