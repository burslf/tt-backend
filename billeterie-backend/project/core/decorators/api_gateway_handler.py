import json
from typing import Callable

from project.core.helpers.custom_log import get_logger

logger = get_logger()


def api_gateway_handler(func) -> Callable:
    def decorated(event, context):
        try:
            endpoint_res = func(event, context)
            endpoint_res = handle_response(body=endpoint_res)

        except Exception as e:
            logger.info(e)

            error_dict = {"code": "OOPS", "description": "Something went wrong."}
            endpoint_res = handle_error(error=error_dict, status_code=503, context=context)

        return endpoint_res

    return decorated


def handle_response(body: dict, status_code=200, context=None, headers=None):
    if headers is None:
        headers = {"Access-Control-Allow-Origin": "*"}

    return {"statusCode": status_code, "headers": headers, "body": json.dumps(body)}


def handle_error(error: dict, status_code: int, context: dict):
    resp = {"statusCode": status_code}
    body = {"error": error, "status": "fail"}

    resp["headers"] = {"Access-Control-Allow-Origin": "*"}
    resp["body"] = json.dumps(body)

    return resp
