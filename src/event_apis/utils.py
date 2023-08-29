from src.event_apis.validators import validate_tracking_plan_events


def get_events_list(data):
    events_list = list()
    if not data:
        return events_list, "rules missing in request data"
    events_list = data.get("events")
    error = ""
    if not events_list:
        error = "events missing in request data"
    if not isinstance(events_list, list):
        error = "events must be a list"
    return events_list, error


def get_tracking_plan_creation_data(data):
    creation_data = dict()
    source = data.get("source")
    name = data.get("display_name")
    description = data.get("description")
    if not (source and name):
        return creation_data
    creation_data.update(source=source, name=name, description=description)
    return creation_data


def get_event_creation_data(data):
    creation_data = {
        "name": data.get("name"),
        "description": data.get("description"),
        "property_details": data.get("data")
    }
    return creation_data


def get_event_updation_data(data):
    updation_data = {
        "description": data.get("description"),
        "property_details": data.get("data")
    }
    return updation_data


def preprocess_events_data(data):
    events_list, error = get_events_list(data)
    if not error:
        events_list, error = validate_tracking_plan_events(events_list)
    return events_list, error


def serialize_event_records(event_records_list=None):
    serialized_records = list()
    event_records_list = event_records_list if event_records_list else []
    if not event_records_list:
        return serialized_records
    for event in event_records_list:
        event_dict = {
            "name": event.name,
            "description": event.description,
            "property_details": event.property_details
        }
        serialized_records.append(event_dict)
    return serialized_records
