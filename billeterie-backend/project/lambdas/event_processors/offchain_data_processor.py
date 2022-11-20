from typing import List

from project.contracts.function_calls.billeterie import get_offchain_uri

from project.core.decorators.fname import fname
from project.core.session import get_session
from project.core.helpers.custom_log import get_logger

from project.db.models import IndexedChainEvent, Network
from project.db.event_created import session_update_created_event
from project.db.index_chain_event import session_get_unprocessed_events_by_network, session_set_event_as_complete
from project.db.network import session_get_networks

logger = get_logger()


@fname
def offchain_data_processor(event, context):
    inner_session = get_session(connection_type="readonly")

    network_objs: List[Network] = session_get_networks(outer_session=inner_session)

    for network_obj in network_objs:
        unprocessed_events: List[IndexedChainEvent]  = session_get_unprocessed_events_by_network(
            outer_session=inner_session,
            network_id=network_obj.id,
            event_name="OffchainDataUpdated"
        )
        
        for unprocessed_event in unprocessed_events:
            event_id = unprocessed_event.dictionary_attributes['eventId']

            offchain_uri = get_offchain_uri(
                event_id=event_id,
                network_obj=network_obj
            )

            session_update_created_event(
                outer_session=inner_session, 
                event_id=event_id,
                update_vals={'offchain_data': offchain_uri}
            )

            session_set_event_as_complete(
                outer_session=inner_session, 
                unprocessed_event_id=unprocessed_event.id
            )

    inner_session.close()
