import logging
import json
from flask import request, Response
from flask.views import MethodView

from src.event_apis.handlers import create_tracking_plan_records, get_all_event_records
from src.event_apis.utils import serialize_event_records, get_default_response_headers
from src.common.utils import get_api_result_dict, save_error_and_return_result


class EventTrackerAPI(MethodView):
    def __init__(self):
        self.request = request

    def post(self):
        result_dict = get_api_result_dict()

        try:
            json_data = request.get_json(force=True)
            print("request data: {}".format(json_data))
            if not json_data:
                return save_error_and_return_result("No input data provided", 422, result_dict)
            tracking_plan = json_data.get("tracking_plan", {})
            created_events, error_details = create_tracking_plan_records(tracking_plan)
            if error_details:
                return save_error_and_return_result(error_details.get("error"), error_details.get("code"),
                                                    result_dict)
            result_dict["result"]["message"] = "success"
            result_dict["result"]["code"] = 201
            response = Response(json.dumps(result_dict, default=str))
            response.headers = get_default_response_headers()
            print("response: {}".format(response))
        except Exception as exc:
            logging.exception(str(exc))
            return save_error_and_return_result("something went wrong", 500, result_dict)
        return response

    def put(self):
        pass

    def get(self):
        result_dict = get_api_result_dict()
        event_records, error_details = get_all_event_records()
        if error_details:
            return save_error_and_return_result(error_details.get("error"), error_details.get("code"),
                                                result_dict)

        serialized_event_records = serialize_event_records(event_records_list=event_records)
        result_dict["result"]["message"] = "success"
        result_dict["result"]["code"] = 200
        result_dict["result"]["records"] = serialized_event_records
        response = Response(json.dumps(result_dict, default=str))
        response.headers = get_default_response_headers()
        print("response: {}".format(response))
        return response
