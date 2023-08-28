import logging
from library.sql.exceptions import SQLAlchemyException
from library.sql.utils import session_wrap, commit_session
from src.event_apis.utils import get_event_creation_data, get_event_updation_data, get_tracking_plan_creation_data, \
    preprocess_events_data
from src.common.utils import validate_json_schema
from src.tracking_planner.events.model_utils import get_event_record_by_name, create_event_record, update_event_record
from src.tracking_planner.tracking_plans.model_utils import get_tracking_plan_record_by_source, \
    create_tracking_plan_record
from src.tracking_planner_transactions.model_utils import get_tracking_plan_transaction_record, \
    create_tracking_plan_transaction_record


@session_wrap
def get_or_create_tracking_plan(data, session=None):
    source = data.get("source", "http")
    tracking_plan_name = data.get("display_name")
    tracking_plan_record = None
    error = ""
    if not tracking_plan_name:
        return tracking_plan_record, error
    tracking_plan_record = get_tracking_plan_record_by_source(source, session=session)
    if not tracking_plan_record:
        creation_data = get_tracking_plan_creation_data(data)
        tracking_plan_record, error = create_tracking_plan_record(creation_data, session=session)
        return tracking_plan_record, error
    if tracking_plan_record and tracking_plan_record.name != tracking_plan_name:
        error = "tracking plan: {} already exists for source, please use it !".format(tracking_plan_record.name)
    return tracking_plan_record, error


@session_wrap
def get_or_create_tracking_plan_transaction(event_record, tracking_plan_record, session=None):
    error = ""
    transaction_ref_id = "{}_{}".format(event_record.id, tracking_plan_record.id)
    transaction_record = get_tracking_plan_transaction_record(transaction_ref_id, session=session)
    if not transaction_record:
        creation_data = {"tracking_plan_id": tracking_plan_record.id, "event_id": event_record.id,
                         "ref_id": transaction_ref_id}
        transaction_record, error = create_tracking_plan_transaction_record(creation_data, session=session)
        if error:
            error = "event: {} could not be linked to plan: {}, reason: {}".\
                format(event_record.name, tracking_plan_record.name, error)
    return transaction_record, error


@session_wrap
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


@session_wrap
def create_tracking_plan_event(data, tracking_plan_record=None, session=None):
    data_records = dict()
    event_schema = data.get("rules")
    event_data = data.get("data")
    error = validate_json_schema(event_data, event_schema)
    if error:
        return data_records, "event: {} could not be created, reason: {}".format(data.get("name"), error)
    creation_data = get_event_creation_data(data)
    event_record, error = create_event_record(creation_data, session=session)
    if error:
        return data_records, "event: {} could not be created, reason: {}".format(data.get("name"), error)
    if tracking_plan_record:
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
    tracking_plan_record, error = get_or_create_tracking_plan(tracking_plan)
    if error:
        return created_event_records, error
    events_list, error = preprocess_events_data(tracking_plan)
    if error:
        return created_event_records, error
    for event_dict in events_list:
        event_name = event_dict.get("name")
        event_record = get_event_record_by_name(event_name)
        if event_record:
            return created_event_records, "event: {} already exists !"
        data_records, error = create_tracking_plan_event(event_dict, tracking_plan_record=tracking_plan_record,
                                                         session=session)
        if error:
            return created_event_records, error
        actioned_event_records.append(data_records.get("event_record"))
    try:
        commit_session(session)
    except SQLAlchemyException as err:
        logging.exception(err)
        return created_event_records, str(err)
    created_event_records = actioned_event_records
    return created_event_records, ""
