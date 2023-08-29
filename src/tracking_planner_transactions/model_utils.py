import logging

from library.sql.exceptions import SQLAlchemyException
from library.sql.utils import add_session_instance, flush_session

from src.tracking_planner_transactions.models import TrackingPlanTransaction


def create_tracking_plan_transaction_record(data, session=None):
    try:
        tracking_plan_transaction_record = TrackingPlanTransaction.create(**data)
        add_session_instance(session, tracking_plan_transaction_record)
        flush_session(session)
    except SQLAlchemyException as exc:
        logging.exception(exc)
        return None, str(exc)
    except ValueError as exc:
        logging.exception(exc)
        return None, str(exc)
    return tracking_plan_transaction_record, ""


def get_all_event_records(tracking_plan_id, session=None):
    event_records = TrackingPlanTransaction.get_all_events_per_tracking_plan(tracking_plan_id, session)
    return event_records


def get_tracking_plan_records(event_id, session=None):
    tracking_plan_records = TrackingPlanTransaction.get_all_tracking_plan_per_event(event_id, session)
    return tracking_plan_records


def get_tracking_plan_transaction_record(ref_id, session=None):
    tracking_plan_transaction_record = TrackingPlanTransaction.get_by_ref_id(ref_id, session)
    return tracking_plan_transaction_record
