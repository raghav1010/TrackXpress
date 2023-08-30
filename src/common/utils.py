import logging
import json
from flask import Response
from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

from src.event_apis.utils import get_default_response_headers


def get_api_result_dict(message=""):
    result_dict = {
        "result": {"message": message},
    }
    return result_dict


def save_error_and_return_result(error, code, result_dict):
    result_dict["error"] = {"message": error, "code": code}
    response = Response(json.dumps(result_dict, default=str))
    response.headers = get_default_response_headers()
    return response


def validate_json_schema(data, jsonschema):
    error = ""
    try:
        validate(instance=data, schema=jsonschema)
    except (ValidationError, SchemaError) as exc:
        logging.exception(str(exc))
        error = str(exc)
    return error
