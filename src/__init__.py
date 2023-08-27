import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade, downgrade
from flask_migrate import migrate as run_migrations

from src.common.env import POSTGRES_INSTANCE_URI

logging.basicConfig(level=logging.INFO)

APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = POSTGRES_INSTANCE_URI
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)


@APP.route("/")
def index_one():
    logging.info(__name__)
    return "Welcome to TrackXpress !"


@APP.route("/migrate_db_up")
def run_upgrade():
    try:
        upgrade(directory='migrations')
        return "Migrations applied, Alembic head upgraded!"
    except Exception as exc:
        logging.exception(str(exc))
        return "Upgrade head failed --- {}".format(str(exc))


@APP.route("/migrate_db_down")
def downgrade_db():
    try:
        downgrade(directory='migrations')
        return "Migrations applied! - Downgrade Done"
    except Exception as exc:
        logging.exception(str(exc))
        return "Downgrade head failed --- {}".format(str(exc))


@APP.route("/run_migrations/<message>")
def run_migrations_db(message=""):
    try:
        run_migrations(directory='migrations', message=message)
        return "Migrations applied, revision generated!"
    except Exception as exc:
        logging.exception(str(exc))
        return "Failed to generate migrations --- {}".format(str(exc))
