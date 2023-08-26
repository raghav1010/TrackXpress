import sys

from flask_migrate import Migrate

from app_config import configure_application
from library.sql.utils import BASE, ENGINE
from src import APP


sys.path.insert(0, "src/")


with APP.app_context():
    configure_application()
    BASE.metadata.create_all(ENGINE, checkfirst=True)
    migrate = Migrate(APP, ENGINE)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=5050, debug=True)
