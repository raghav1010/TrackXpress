import logging
from logging.config import dictConfig
import sys

from flask_migrate import Migrate

from app_config import configure_application
from library.sql.utils import BASE, ENGINE
from src import APP

dictConfig({
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
        })
logging.basicConfig(level=logging.DEBUG)

with APP.app_context():
    configure_application()
    BASE.metadata.create_all(ENGINE, checkfirst=True)
    migrate = Migrate(APP, ENGINE)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5050, debug=True)
