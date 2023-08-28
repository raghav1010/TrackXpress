def validate_tracking_plan_events(events_list):
    error = ""
    for event in events_list:
        event_rules = event.get("rules")
        event_name = event.get("name")
        event_data = event.get("data")
        if not all(event_data, event_rules, event_name):
            error = "each event must contain name, rules, data"
            return events_list, error
    return events_list, error
