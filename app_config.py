import logging
from flask import request
from src.routes import *
from src import APP


def configure_api_logs():
    def log_requests():
        try:
            logging.info("=============================================")
            logging.info(">>{}".format(request))
            logging.info(">>Request Headers: {}".format(request.headers))
            logging.info(">>Request Data: {}".format((request.data or "")))
            logging.info(">>Request Params: {}".format(request.args))
            logging.info("=============================================")
        except Exception as e:
            logging.error(">>Request Error: {}".format(e))

    def log_responses(response):
        try:
            logging.info("=============================================")
            logging.info(">>{}".format(response))
            logging.info(">>Response headers: {}".format(response.headers))
            logging.info(">>Response data: {}".format((response.data or "")))
        except Exception as err:
            logging.error(">>Response Error: {}".format(err))
        return response

    APP.before_request(log_requests)
    APP.after_request(log_responses)


def configure_application():
    configure_app_routes()
    configure_api_logs()
