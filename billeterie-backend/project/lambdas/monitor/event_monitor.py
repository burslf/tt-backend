import json

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

    network_objs: [Network] = session_get_networks(outer_session=inner_session)

    inner_session.close()

    events_to_monitor = {
        "EventCreated": "event_created_monitor",
        # "OffchainDataUpdated": "offchain_monitor",
        # "OptionAdded": "option_added_monitor",
        # "OptionRemoved": "option_removed_monitor",
        # "TransferSingle": "mint_monitor",
    }

    for network in network_objs:
        for event_name, event_monitor_name in events_to_monitor.items():
            try:
                message = get_sqs_message(function_name=event_monitor_name,
                                          message_body={'network_name': network.name, 'event_name': event_name})
                send_message(queue_name=f'{network.name.lower()}_{event_monitor_name}', messages=[message])
                logger.info(f'SUCCESSFULLY CALLED SQS EVENT: {network.name.lower()}_{event_monitor_name}')
            except Exception as e:
                logger.info(e)
                error_message = json.dumps(e)
                message: json.dumps(e)
                send_slack_message(message=error_message)

    logger.info("SLEEPING FOR NOW...")
