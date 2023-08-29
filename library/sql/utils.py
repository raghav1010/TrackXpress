import logging


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, session as session_orm
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, InvalidRequestError, DataError, OperationalError

from library.sql.exceptions import SQLAlchemyException
from src.common.env import POSTGRES_INSTANCE_URI

ENGINE = create_engine(POSTGRES_INSTANCE_URI)
SESSION = sessionmaker(bind=ENGINE)
BASE = declarative_base()


def session_wrap(function_handler):
    def wrap(*args, **kwargs):
        close_session = False

        # if session already present then reuse the session instead of creating new
        if args and isinstance(args[-1], session_orm.Session):
            session = args[-1]
            kwargs["session"] = session
            args = args[:-1]
        else:
            session = SESSION()
            kwargs["session"] = session
            logging.info("created session instance -> {}".format(session))
            close_session = True
        print("session is: {}".format(session))
        print("func handler: {}".format(function_handler.__name__))
        try:
            result = function_handler(*args, **kwargs)
        except Exception as err:
            session.rollback()
            error_msg = "Postgres Commit Error: {}".format(str(err))
            logging.error(error_msg)
            raise SQLAlchemyException(error_msg)
        finally:
            if close_session:
                logging.info("closing session instance -> {}".format(session))
                session.close()

        return result
    return wrap


def commit_session(session):
    try:
        session.commit()
    except (IntegrityError, DataError, InvalidRequestError, OperationalError, SQLAlchemyError) as exc:
        error_msg = "Database Commit SQLAlchemy Error: {}".format(str(exc))
        logging.exception(error_msg)
        rollback_session(session)
        raise SQLAlchemyException(error_msg)
    except Exception as exc:
        error_msg = "Database Commit Generic Error: {}".format(str(exc))
        logging.exception(error_msg)
        rollback_session(session)
        raise SQLAlchemyException(error_msg)


def flush_session(session, _objects=None):
    try:
        session.flush(objects=_objects)
    except (IntegrityError, DataError, InvalidRequestError, OperationalError, SQLAlchemyError) as exc:
        error_msg = "Database Flush SQLAlchemy Error: {}".format(str(exc))
        logging.exception(error_msg)
        rollback_session(session)
        raise SQLAlchemyException(error_msg)
    except Exception as exc:
        error_msg = "Database Flush Generic Error: {}".format(str(exc))
        logging.exception(error_msg)
        rollback_session(session)
        raise SQLAlchemyException(error_msg)


def add_session_instance(session, instance, _warn=True):
    try:
        session.add(instance, _warn=_warn)
    except (IntegrityError, DataError, InvalidRequestError, OperationalError, SQLAlchemyError) as exc:
        error_msg = "Database Session Add SQLAlchemy Error: {}".format(str(exc))
        logging.exception(error_msg)
        rollback_session(session)
        raise SQLAlchemyException(error_msg)
    except Exception as exc:
        error_msg = "Database Session Add Generic Error: {}".format(str(exc))
        logging.exception(error_msg)
        rollback_session(session)
        raise SQLAlchemyException(error_msg)


def rollback_session(session):
    try:
        session.rollback()
    except (InvalidRequestError, OperationalError, SQLAlchemyError) as exc:
        error_msg = "Database Rollback SQLAlchemy Error: {}".format(str(exc))
        logging.exception(error_msg)
        raise SQLAlchemyException(error_msg)
    except Exception as exc:
        error_msg = "Database Rollback Generic Error: {}".format(str(exc))
        logging.exception(error_msg)
        raise SQLAlchemyException(error_msg)


def refresh_session_instance(session, instance, _attribute_names=None, _with_for_update=None):
    try:
        session.refresh(instance, attribute_names=_attribute_names, with_for_update=_with_for_update)
    except (IntegrityError, DataError, InvalidRequestError, OperationalError, SQLAlchemyError) as exc:
        error_msg = "Database Session Refresh SQLAlchemy Error: {}".format(str(exc))
        logging.exception(error_msg)
        raise SQLAlchemyException(error_msg)
    except Exception as exc:
        error_msg = "Database Session Refresh Generic Error: {}".format(str(exc))
        logging.exception(error_msg)
        raise SQLAlchemyException(error_msg)


def sql_check_choices(self, key, value, choices):
    if value in choices:
        return value
    raise ValueError("'{}' is not a valid choice for '{}' column in '{}' table"
                     .format(value, key, type(self).__name__))
