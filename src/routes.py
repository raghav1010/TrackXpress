from src import APP
from src.event_apis import API_ROUTES as EVENT_API_ROUTES


func_based_routes = ''

class_based_routes = EVENT_API_ROUTES


def configure_app_routes():
    for route in func_based_routes:
        api_url = route[0]
        handler = route[1]
        methods = route[2]
        APP.add_url_rule(api_url, "{}|{}".format(route, handler), handler, methods=methods)

    for route in class_based_routes:
        api_url = route[0]
        methods = route[1]
        view_function = route[2]
        APP.add_url_rule(api_url, methods=methods, view_func=view_function)
