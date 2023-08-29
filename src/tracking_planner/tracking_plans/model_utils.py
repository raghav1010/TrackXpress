import logging

from library.sql.exceptions import SQLAlchemyException
from library.sql.utils import session_wrap, add_session_instance, flush_session

from .models import TrackingPlan



def create_tracking_plan_record(data, session=None):
    try:
        tracking_plan_record = TrackingPlan.create(**data)
        add_session_instance(session, tracking_plan_record)
        flush_session(session)
    except SQLAlchemyException as exc:
        logging.exception(exc)
        return None, str(exc)
    except ValueError as exc:
        logging.exception(exc)
        return None, str(exc)
    return tracking_plan_record, ""



def get_tracking_plan_record_by_id(tracking_plan_id, session=None):
    tracking_plan_record = TrackingPlan.get_by_id(tracking_plan_id, session)
    return tracking_plan_record



def get_tracking_plan_record_by_source(source, session=None):
    tracking_plan_record = TrackingPlan.get_by_source(source, session)
    return tracking_plan_record


def get_tracking_plan_record_by_name(name, session=None):
    tracking_plan_record = TrackingPlan.get_by_name(name, session)
    return tracking_plan_record
