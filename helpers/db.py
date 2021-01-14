from sqlalchemy import create_engine
from models.base import Base
from conf.settings import config


def load_db():
    engine = create_engine(config.SQLITE_PREFIX + config.SQLITEDB, echo=True)
    Base.metadata.create_all(engine)
