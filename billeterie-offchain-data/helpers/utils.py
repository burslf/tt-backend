
def get_from_query_params(event: dict, param: str):
    query = None
    query_params = event.get("queryStringParameters", None)
    if query_params is not None:
        query = query_params.get(param, None)
    return query


def get_s3_link(bucket_name=None, key=None):
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"