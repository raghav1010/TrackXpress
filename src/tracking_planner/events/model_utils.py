import logging

from library.sql.exceptions import SQLAlchemyException
from library.sql.utils import session_wrap, add_session_instance, flush_session

from .models import Event


@session_wrap
def create_event_record(data, session=None):
    try:
        event_record = Event.create(**data)
        add_session_instance(session, event_record)
        flush_session(session)
    except SQLAlchemyException as exc:
        logging.exception(exc)
        return None, str(exc)
    except ValueError as exc:
        logging.exception(exc)
        return None, str(exc)
    return event_record, ""


@session_wrap
def update_event_record(event_record, data, session=None):
    try:
        event_record.update(**data)
        add_session_instance(session, event_record)
        flush_session(session)
    except SQLAlchemyException as exc:
        logging.exception(exc)
        return event_record, str(exc)
    except ValueError as exc:
        logging.exception(exc)
        return event_record, str(exc)
    return event_record, ""


@session_wrap
def get_event_record_by_id(event_id, session=None):
    event_record = Event.get_by_id(event_id, session)
    return event_record


@session_wrap
def get_event_record_by_name(name, session=None):
    event_record = Event.get_by_name(name, session)
    return event_record
