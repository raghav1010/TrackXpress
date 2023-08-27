def get_events_list(data):
    events_list = list()
    if not data:
        return events_list, "tracking_plan missing in request data"
    events_list = data.get("rules", {}).get("events")
    error = ""
    if not events_list:
        error = "events_list missing in request data"
    if not isinstance(events_list, list):
        error = "events_list must be a list"
    return events_list, error


def get_tracking_plan_creation_data(data):
    creation_data = {
        "source": data.get("source"),
        "name": data.get("display_name")
    }
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
