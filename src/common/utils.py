import logging

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError


def get_api_result_dict(message=""):
    result_dict = {
        "result": {"message": message},
    }
    return result_dict


def save_error_and_return_result(error, code, result_dict):
    result_dict["error"] = {"message": error, "code": code}
    return result_dict


def validate_json_schema(data, jsonschema):
    print("data: {}, jsonschema: {}".format(data, jsonschema))
    error = ""
    try:
        validate(instance=data, schema=jsonschema)
    except (ValidationError, SchemaError) as exc:
        logging.exception(str(exc))
        error = str(exc)
    return error
