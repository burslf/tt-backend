import json
import logging

import boto3

from helpers.utils import get_from_query_params, get_s3_link

logger = logging.getLogger()
logger.setLevel("INFO")


def get_offchain_data(event: {}, context: {}):
    token_id = get_from_query_params(event=event, param="token_id")

    s3 = boto3.resource('s3')
    s3object = s3.Object("ticketrust-develop", f"metadata/{token_id}.json")

    try:
        data = s3object.get()["Body"].read().decode("utf-8")
        json_data = json.loads(data)

        return {
            "statusCode": 200,
            "body": json.dumps(json_data)
        }
    except Exception as e:
        logger.info(e)
        return {
            "statusCode": 400,
            "body": "not found"
        }

