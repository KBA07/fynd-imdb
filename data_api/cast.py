from data_api.models import Cast


def get_cast(session, name):
    return session.query(Cast).filter(Cast.name == name).first()


def add_cast(session, name):
    cast_obj = Cast(name)
    session.add(cast_obj)
    return cast_obj