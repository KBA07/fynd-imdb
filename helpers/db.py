from contextlib import contextmanager

from sqlalchemy import create_engine
from data_api.base import Base
from conf.settings import config

from sqlalchemy.orm import Session


def get_engine():
    return create_engine(config.SQLITE_PREFIX + config.SQLITEDB, echo=True)


def load_db():
    engine = get_engine()
    Base.metadata.create_all(engine)


def session():
    # Return sqlalchemy session to database
    return Session(bind=get_engine(), expire_on_commit=False)


@contextmanager
def terminating_sn():
    # A contextlib which closes session and db connections after use
    sn = session()
    try:
        yield sn
    finally:
        sn.close()
        sn.bind.dispose()
