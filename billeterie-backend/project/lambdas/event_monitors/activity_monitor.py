import json
from typing import List

from project.core.decorators.fname import fname
from project.core.session import get_session
from project.core.helpers.custom_log import get_logger
from project.core.helpers.slack_message import send_slack_message
from project.db.models import Network
from project.db.network import session_get_networks
from project.general.sqs import get_sqs_message, send_message

logger = get_logger()


@fname
def event_monitor(event, context):
    inner_session = get_session(connection_type="readonly")

    network_objs: List[Network] = session_get_networks(outer_session=inner_session)

    inner_session.close()

    events_to_monitor = ["EventCreated", "OffchainDataUpdated", "OptionAdded", "OptionRemoved", "TransferSingle" ]
    sqs_event_monitor_name = "event_monitor"

    for network in network_objs:
        for event_name in events_to_monitor:
            try:
                message = get_sqs_message(function_name=sqs_event_monitor_name,
                                          message_body={'network_name': network.name, 'event_name': event_name})
                send_message(queue_name=f'{network.name.lower()}_{sqs_event_monitor_name}', messages=[message])

                logger.info(f'CALLED SQS EVENT MONITOR FOR : {network.name.lower()}')
            except Exception as e:
                logger.info(e)
                error_message = json.dumps(e)
                message: json.dumps(e)
                send_slack_message(message=error_message)

    logger.info("SLEEPING FOR NOW...")
