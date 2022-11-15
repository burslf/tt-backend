import json
import os


import requests
from requests.exceptions import HTTPError, InvalidURL

from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.core.helpers.utils import get_time_now

HOOK_URL = os.environ["SLACK_HOOK_URL"]

logger = get_logger()

now = get_time_now()

logger.info(now)

slack_id_by_members = {
    "Yoel": "U03QCF9V25B",
}


def get_member_id_by_name(member_name: str):
    member_name = slack_id_by_members.get(member_name)
    return member_name


@fname
def send_slack_message(message: str, channel: str = "alerts-test", mentions: [] = [], color: str = None):
    data = {'channel': channel}

    for member_name in mentions:
        member = get_member_id_by_name(member_name=member_name)
        message += f' <@{member}> '

    if color:
        data["attachments"] = [
            {
                "color": color,
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": message,
                        },
                    }
                ],
            }
        ]
    else:
        data["text"] = message

    try:
        requests.post(url=HOOK_URL, data=json.dumps(data))
        logger.info("Message posted")

    except Exception as e:
        logger.error("Server connection failed: %s", e)