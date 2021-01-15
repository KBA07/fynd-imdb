
class Config(object):
    SQLITE_PREFIX = "sqlite:///"
    SQLITEDB = "inventory.db"
    # Copying the configuration below from flask documentation
    FLASK_LOG_CONFIGURATION = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    }
    # TODO: Bad practice This Should be ideally populated at runtime
    EDIT_USER_MAP = {"admin": "admin"}
