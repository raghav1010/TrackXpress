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
        try:
            if not json_data:
                return save_error_and_return_result("No input data provided", 422, result_dict)
            tracking_plan = json_data.get("tracking_plan", {})
            created_events, error_details = create_tracking_plan_records(tracking_plan)
            if error_details:
                return save_error_and_return_result(error_details.get("error"), error_details.get("code"),
                                                    result_dict)
            serialized_event_records = serialize_event_records(event_records_list=created_events)
            result_dict["result"]["message"] = "success"
            result_dict["result"]["code"] = 201
            result_dict["result"]["records"] = serialized_event_records
        except Exception as exc:
            logging.exception(str(exc))
            return save_error_and_return_result("something went wrong", 500, result_dict)
        return result_dict

    def put(self):
        pass

    def get(self):
        pass



