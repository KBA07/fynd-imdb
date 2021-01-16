
class InputOutOfBounds(Exception):
    pass


class Validator(object):
    MAX_LIMIT = 100
    DEFAULT_LIMIT = 20
    DEFAULT_OFFSET = 0

    @staticmethod
    def get_limit_offset(limit, offset):
        if limit and limit > Validator.MAX_LIMIT or limit < 0:
            limit = Validator.MAX_LIMIT

        if not offset or offset < 0:
            offset = 0

        return limit, offset

    @staticmethod
    def validate_param(popularity, imdb_score):
        if popularity > 100 or popularity < 0:
            # raise validation error
            raise InputOutOfBounds

        if imdb_score > 10 or imdb_score < 0:
            # raise validation error
            raise InputOutOfBounds
