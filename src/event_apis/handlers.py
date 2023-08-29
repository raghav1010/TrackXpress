import logging

from library.sql.exceptions import SQLAlchemyException
from library.sql.utils import session_wrap, commit_session, refresh_session_instance
from src.event_apis.utils import get_event_creation_data, get_event_updation_data, get_tracking_plan_creation_data, \
    preprocess_events_data
from src.common.utils import validate_json_schema
from src.tracking_planner.events.model_utils import get_event_record_by_name, create_event_record, update_event_record, \
    get_all_events
from src.tracking_planner.tracking_plans.model_utils import get_tracking_plan_record_by_source, \
    create_tracking_plan_record, get_tracking_plan_record_by_name
from src.tracking_planner_transactions.model_utils import get_tracking_plan_transaction_record, \
    create_tracking_plan_transaction_record


def get_or_create_tracking_plan(data, session=None):
    tracking_plan_record = None
    error = ""
    creation_data = get_tracking_plan_creation_data(data)
    print("creation_data: {}".format(creation_data))
    if not creation_data:
        if data.get("description"):
            error = "tracking plan must have display_name and source"
        return tracking_plan_record, error
    tracking_plan_record = get_tracking_plan_record_by_source(creation_data.get("source"), session=session)
    if tracking_plan_record:
        return tracking_plan_record, "tracking plan: {} already exists for source!"\
            .format(tracking_plan_record.name)
    tracking_plan_record = get_tracking_plan_record_by_name(creation_data.get("name"), session=session)
    if tracking_plan_record:
        return tracking_plan_record, "tracking plan: {} already exists for source: {}!"\
            .format(tracking_plan_record.name, tracking_plan_record.source)
    tracking_plan_record, error = create_tracking_plan_record(creation_data, session=session)
    return tracking_plan_record, error


def get_or_create_tracking_plan_transaction(event_record, tracking_plan_record, session=None):
    error = ""
    transaction_ref_id = "{}_{}".format(event_record.name, tracking_plan_record.name)
    print("transaction_ref_id: {}".format(transaction_ref_id))
    transaction_record = get_tracking_plan_transaction_record(transaction_ref_id, session=session)
    if transaction_record:
        print("existing transaction record: {}".format(transaction_record))
        return transaction_record, error
    creation_data = {"tracking_plan_id": tracking_plan_record.id, "event_id": event_record.id,
                     "ref_id": transaction_ref_id}
    transaction_record, error = create_tracking_plan_transaction_record(creation_data, session=session)
    try:
        commit_session(session)
        refresh_session_instance(session, tracking_plan_record)
    except SQLAlchemyException as exc:
        return transaction_record, "event: {} could not be linked to tracking plan: {}, reason: {}".\
            format(event_record.name, tracking_plan_record.name, str(exc))
    if error:
        error = "event: {} could not be linked to plan: {}, reason: {}".\
            format(event_record.name, tracking_plan_record.name, error)
    print("created transaction record: {}".format(transaction_record))
    return transaction_record, error


def update_tracking_plan_event(event_record, data, session=None):
    event_schema = data.get("rules")
    event_data = data.get("data")
    error = validate_json_schema(event_data, event_schema)
    if error:
        return event_record, error
    updation_data = get_event_updation_data(data)
    event_record, error = update_event_record(event_record, updation_data, session=session)
    if error:
        error = "event: {} could not be updated, reason: {}".format(event_record.name, error)
    return event_record, error


def create_tracking_plan_event(data, tracking_plan_record=None, session=None):
    data_records = dict()
    event_schema = data.get("rules", {}).get("properties", {})
    event_data = data.get("data")
    error = validate_json_schema(event_data, event_schema)
    if error:
        return data_records, "event: {} could not be created, reason: {}".format(data.get("name"), error)
    creation_data = get_event_creation_data(data)
    event_record, error = create_event_record(creation_data, session=session)
    if error:
        return data_records, "event: {} could not be created, reason: {}".format(data.get("name"), error)
    try:
        commit_session(session)
        refresh_session_instance(session, event_record)
        if tracking_plan_record:
            refresh_session_instance(session, tracking_plan_record)
    except SQLAlchemyException as exc:
        return data_records, "event: {} could not be created, reason: {}".format(data.get("name"), str(exc))
    if tracking_plan_record:
        print("here------------------------")
        transaction_record, error = get_or_create_tracking_plan_transaction(event_record, tracking_plan_record,
                                                                            session=session)
        if error:
            return data_records, "event: {} could not be created, reason: {}".format(data.get("name"), error)
        data_records["transaction_record"] = transaction_record
    data_records["event_record"] = event_record
    return data_records, error


@session_wrap
def create_tracking_plan_records(tracking_plan, session=None):
    actioned_event_records = list()
    created_event_records = list()
    tracking_plan_record, error = get_or_create_tracking_plan(tracking_plan, session=session)
    if error:
        return created_event_records, {"error": error, "code": 401}
    events_list, error = preprocess_events_data(tracking_plan.get("rules"))
    if error:
        return created_event_records, {"error": error, "code": 422}
    for event_dict in events_list:
        event_record = get_event_record_by_name(event_dict.get("name"), session=session)
        if event_record:
            return created_event_records, {"error": "event: {} already exists !".format(event_dict.get("name")),
                                           "code": 422}

        data_records, error = create_tracking_plan_event(event_dict, tracking_plan_record=tracking_plan_record,
                                                         session=session)
        if error:
            return created_event_records, {"error": error, "code": 401}
        actioned_event_records.append(data_records.get("event_record"))
    print("actioned_event_records: {}".format(data_records))
    created_event_records = actioned_event_records
    return created_event_records, dict()


@session_wrap
def get_all_event_records(session=None):
    event_records = list()
    error_dict = dict()
    try:
        event_records = get_all_events(session=session)
    except Exception as exc:
        logging.exception(str(exc))
        error_dict = {"error": "No records found", "code": 400}
    return event_records, error_dict
