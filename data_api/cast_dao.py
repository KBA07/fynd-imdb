from data_api.models import Cast


class CastDao(object):
    @staticmethod
    def get_cast(session, name):
        return session.query(Cast).filter(Cast.name == name).first()

    @staticmethod
    def add_cast(session, name):
        cast_obj = Cast(name)
        session.add(cast_obj)
        return cast_obj

    @staticmethod
    def check_or_add_cast(session, cast_name):
        cast_obj = CastDao.get_cast(session, cast_name)

        if not cast_obj:
            cast_obj = CastDao.add_cast(session, cast_name)
            session.flush()
        return cast_obj
