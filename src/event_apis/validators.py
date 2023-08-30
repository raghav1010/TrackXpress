import json


def validate_tracking_plan_events(events_list):
    error = ""
    for event in events_list:
        event_rules = event.get("rules")
        event_name = event.get("name")
        if not all([event_rules, event_name]):
            return events_list, "each event must have name, rules,"
        if not validate_event_rules(event_rules):
            return events_list, "event rules not in order, must have properties, required, data"
    return events_list, error


def validate_event_rules(rules):
    rules = json.loads(rules)
    properties = rules.get("properties", {}).get("properties")
    required = rules.get("properties", {}).get("required")
    data = rules.get("properties", {}).get("data")
    if not (properties and required and data):
        return False
    return True
