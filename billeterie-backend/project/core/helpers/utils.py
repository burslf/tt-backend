from datetime import datetime, timezone


def get_time_now():
    utc_now = datetime.now(timezone.utc).isoformat()
    return utc_now


def get_from_query_params(event: dict, param: str):
    query = None
    query_params = event.get("queryStringParameters", None)
    if query_params is not None:
        query = query_params.get(param, None)
    return query

