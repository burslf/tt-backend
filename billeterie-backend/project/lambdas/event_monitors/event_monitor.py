import json
import os
from typing import Dict

from project.contracts.abis.billeterie_abi import billeterie_abi
from project.core.helpers.custom_log import get_logger
from project.core.helpers.slack_message import send_slack_message
from project.core.session import get_session
from project.core.web3.events_helpers import get_all_latest_events
from project.core.web3.web3_helpers import get_web3_instance
from project.db.index_chain_event import session_get_latest_event_scanned_by_event_and_network, session_add_new_event
from project.db.network import session_get_network_details_by_name
from project.general.chains_configs import contract_addresses, contract_creation_block

logger = get_logger()


def event_monitor(event: Dict, context: Dict, network_dict=None):
    records = event.get("Records")

    if records is None:
        raise Exception("Records is None")

    queue_event = records[0]

    body = json.loads(queue_event.get("body"))

    network_name = body.get("network_name")
    event_name = body.get("event_name")

    print(f"EVENT TRIGGERED FOR NETWORK: {network_name}")

    env = os.environ["ENV"]

    inner_session = get_session(connection_type="readonly")

    network_obj = session_get_network_details_by_name(outer_session=inner_session, network_name=network_name)

    billeterie_address = contract_addresses["billeterie"][env][network_name]

    web3 = get_web3_instance(rpc_url=network_obj.rpc_url)

    latest_event_from_db = session_get_latest_event_scanned_by_event_and_network(outer_session=inner_session,
                                                                                 event_name=event_name,
                                                                                 network_id=int(network_obj.id))

    # # If not such event in db, check from contract creation block
    if latest_event_from_db is not None:
        block_number = latest_event_from_db.block_number+1
        logger.info(f'FETCHING FROM LATEST EVENT SCANNED: {block_number}...')
    else:
        block_number = contract_creation_block[env][network_name]

    latest_events = get_all_latest_events(web3=web3, from_block=int(block_number), event_name=event_name,
                                          network_name=network_name, contract_address=billeterie_address,
                                          abi=billeterie_abi)

    for event in latest_events:
        add_new_event_in_db = session_add_new_event(outer_session=inner_session, event_name=event["event_name"],
                                                    contract_address=billeterie_address, dict_attr=event["args"],
                                                    block_number=event["block_number"], tx_hash=event["tx_hash"],
                                                    network_id=network_obj.id)

        new_event_dict = add_new_event_in_db.as_dict()

        logger.info(f'NEW EVENT FOUND: {new_event_dict}')
        message = f'New event found: {add_new_event_in_db.event_name}' \
                  f' <{network_obj.block_scanner_url}/tx/{add_new_event_in_db.tx_hash}>'

        send_slack_message(message=message)

    inner_session.commit()
    inner_session.close()

    logger.info("SLEEPING FOR NOW...")
