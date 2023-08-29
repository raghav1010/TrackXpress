def validate_tracking_plan_events(events_list):
    error = ""
    for event in events_list:
        event_rules = event.get("rules")
        event_name = event.get("name")
        event_data = event.get("data")
        if not all([event_data, event_rules, event_name]):
            return events_list, "each event must have name, rules, data"
        if not validate_event_rules(event_rules):
            return events_list, "event rules not in order"
    return events_list, error


def validate_event_rules(rules):
    properties = rules.get("properties", {}).get("properties")
    required = rules.get("properties", {}).get("required")
    if not (properties and required):
        return False
    return True
