import json
from typing import List

from project.contracts.function_calls.billeterie import get_offchain_uri, get_payees

from project.db.models import IndexedChainEvent
from project.db.event_created import session_add_new_created_event
from project.db.index_chain_event import session_get_unprocessed_events_by_network, session_set_event_as_complete

from project.core.decorators.fname import fname
from project.core.session import get_session
from project.core.helpers.custom_log import get_logger
from project.core.helpers.slack_message import send_slack_message
from project.db.models import Network
from project.db.network import session_get_networks
from project.general.sqs import get_sqs_message, send_message

logger = get_logger()


@fname
def event_created_processor(event, context):
    inner_session = get_session(connection_type="readonly")

    network_objs: List[Network] = session_get_networks(outer_session=inner_session)

    for network_obj in network_objs:
        unprocessed_events: List[IndexedChainEvent]  = session_get_unprocessed_events_by_network(
            outer_session=inner_session,
            network_id=network_obj.id,
            event_name="EventCreated"
        )
        
        for unprocessed_event in unprocessed_events:
            created_event_shares = get_payees(
                event_id=unprocessed_event.dictionary_attributes['id'], 
                creator=unprocessed_event.dictionary_attributes['owner'], 
                network_obj=network_obj
            )
            offchain_uri = get_offchain_uri(
                event_id=unprocessed_event.dictionary_attributes['id'],
                network_obj=network_obj
            )

            session_add_new_created_event(
                outer_session=inner_session,
                indexed_chain_event_id=unprocessed_event.id,
                tx_hash=unprocessed_event.tx_hash,
                network_id=unprocessed_event.network_id,
                event_id=unprocessed_event.dictionary_attributes['id'],
                creator=unprocessed_event.dictionary_attributes['owner'],
                tickets_total=unprocessed_event.dictionary_attributes['initialSupply'],
                tickets_left=unprocessed_event.dictionary_attributes['initialSupply'],
                event_date=unprocessed_event.dictionary_attributes['eventDate'],
                options_fees=unprocessed_event.dictionary_attributes['optionFees'],
                grey_market_allowed=unprocessed_event.dictionary_attributes['greyMarketAllowed'],
                offchain_data=offchain_uri,
                shares=created_event_shares,
                price=unprocessed_event.dictionary_attributes['price'],
            )

            session_set_event_as_complete(
                outer_session=inner_session, 
                unprocessed_event_id=unprocessed_event.id
            )

    inner_session.close()
