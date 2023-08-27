from library.sql.utils import session_wrap
from src.apis.utils import get_events_list, get_event_creation_data, get_event_updation_data, \
    get_tracking_plan_creation_data
from src.apis.validators import validate_tracking_plan_events
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
def create_tracking_plan_event(data, session=None):
    event_record = None
    event_schema = data.get("rules")
    event_data = data.get("data")
    error = validate_json_schema(event_data, event_schema)
    if error:
        return event_record, error
    creation_data = get_event_creation_data(data)
    event_record, error = create_event_record(creation_data, session=session)
    if error:
        error = "event: {} could not be created, reason: {}".format(data.get("name"), error)
    return event_record, error


@session_wrap
def upsert_tracking_plan_events(tracking_plan, session=None):
    actioned_events_list = list()
    error_list = list()
    tracking_plan_record, error = get_or_create_tracking_plan(tracking_plan)
    if error:
        return actioned_events_list, error
    events_list, error = get_events_list(tracking_plan)
    if error:
        return actioned_events_list, error
    events_list, error = validate_tracking_plan_events(events_list)
    if error:
        return actioned_events_list, error
    for event_dict in events_list:
        event_name = event_dict.get("name")
        event_record = get_event_record_by_name(event_name)
        if event_record:
            event_record, error = update_tracking_plan_event(event_record, event_dict, session=session)
        else:
            event_record, error = create_tracking_plan_event(event_dict, session=session)
        if not error:
            actioned_events_list.append(event_record)
            transaction_record, error = get_or_create_tracking_plan_transaction(event_record, tracking_plan_record)
        if error:
            error_list.append(error)
    error = "\n".join(error for error in error_list)
    return actioned_events_list, error
