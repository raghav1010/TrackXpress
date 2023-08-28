import logging
from flask import request
from flask.views import MethodView

from src.event_apis.handlers import create_tracking_plan_records
from src.event_apis.utils import serialize_event_records
from src.common.utils import get_api_result_dict, save_error_and_return_result


class EventTrackerAPI(MethodView):
    def __init__(self):
        self.request = request

    def post(self):
        json_data = request.get_json(force=True)
        result_dict = get_api_result_dict()
        if not json_data:
            return save_error_and_return_result("No input data provided", 400, result_dict)
        tracking_plan = json_data.get("tracking_plan")
        created_events, error = create_tracking_plan_records(tracking_plan)
        if error:
            return save_error_and_return_result(error, 401, result_dict)
        serialized_event_records = serialize_event_records(event_records_list=created_events)
        result_dict["result"]["message"] = "success"
        result_dict["result"]["code"] = 201
        result_dict["result"]["content"] = serialized_event_records
        return result_dict

    def put(self):
        pass

    def get(self):
        pass



