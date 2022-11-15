import json
import os

import boto3
from botocore.config import Config

from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger

logger = get_logger()
config = Config(connect_timeout=5, retries={'max_attempts': 20})


@fname
def get_sqs_message(function_name: str, message_body: dict) -> dict:
    message = {"Id": f"u-{function_name}", "MessageBody": json.dumps(message_body)}

    logger.info(f"sqs message: {message}")

    return message


@fname
def get_sqs_client_by_name(queue_name=None):
    sqs = boto3.resource('sqs', config=config)

    env = os.environ["ENV"]

    queue = sqs.get_queue_by_name(QueueName=f'{env}_{queue_name}')

    return queue


@fname
def send_message(queue_name: str, messages: [dict]):
    queue = get_sqs_client_by_name(queue_name=queue_name)
    queue.send_messages(Entries=messages)
