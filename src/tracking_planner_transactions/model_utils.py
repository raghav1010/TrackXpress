import logging

from library.sql.exceptions import SQLAlchemyException
from library.sql.utils import session_wrap, add_session_instance, commit_session, refresh_session_instance

from src.tracking_planner_transactions.models import TrackingPlanTransaction


@session_wrap
def create_tracking_plan_transaction_record(data, session=None):
    try:
        tracking_plan_transaction_record = TrackingPlanTransaction.create(**data)
        add_session_instance(session, tracking_plan_transaction_record)
        commit_session(session)
        refresh_session_instance(session, tracking_plan_transaction_record)
    except SQLAlchemyException as exc:
        logging.exception(exc)
        return None, str(exc)
    except ValueError as exc:
        logging.exception(exc)
        return None, str(exc)
    return tracking_plan_transaction_record, ""


@session_wrap
def get_all_event_records(tracking_plan_id, session=None):
    event_records = TrackingPlanTransaction.get_all_events_per_tracking_plan(tracking_plan_id, session)
    return event_records


@session_wrap
def get_tracking_plan_records(event_id, session=None):
    tracking_plan_records = TrackingPlanTransaction.get_all_tracking_plan_per_event(event_id, session)
    return tracking_plan_records


def get_tracking_plan_transaction_record(ref_id, session=None):
    tracking_plan_transaction_record = TrackingPlanTransaction.get_by_ref_id(ref_id, session)
    return tracking_plan_transaction_record
