from data_api.models import Cast


def get_cast(session, name):
    return session.query(Cast).filter(Cast.name == name).first()


def add_cast(session, name):
    cast_obj = Cast(name)
    session.add(cast_obj)
    return cast_obj


def check_or_add_cast(session, cast_name):
    cast_obj = get_cast(session, cast_name)

    if not cast_obj:
        cast_obj = add_cast(session, cast_name)
        session.flush()
    return cast_obj
