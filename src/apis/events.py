import logging
from flask import request
from flask.views import MethodView

from src.apis.handlers import upsert_tracking_plan_events
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
        actioned_events_list, error = upsert_tracking_plan_events(tracking_plan)
        if error:
            return save_error_and_return_result(error, 401, result_dict)
        result_dict["result"]["message"] = "success"
        result_dict["result"]["code"] = 204
        return result_dict



