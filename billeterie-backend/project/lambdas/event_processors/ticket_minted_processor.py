from typing import List


from project.core.decorators.fname import fname
from project.core.session import get_session
from project.core.helpers.custom_log import get_logger

from project.db.models import IndexedChainEvent, Network
from project.db.index_chain_event import session_get_unprocessed_events_by_network, session_set_event_as_complete
from project.db.network import session_get_networks
from project.db.event_created import session_get_created_event_by_event_id, session_update_created_event
from project.db.ticket_minted import session_add_new_ticket_minted

logger = get_logger()


@fname
def ticket_minted_processor(event, context):
    inner_session = get_session(connection_type="readonly")

    network_objs: List[Network] = session_get_networks(outer_session=inner_session)

    for network_obj in network_objs:
        unprocessed_events: List[IndexedChainEvent]  = session_get_unprocessed_events_by_network(
            outer_session=inner_session,
            network_id=network_obj.id,
            event_name="TransferSingle"
        )
        
        for unprocessed_event in unprocessed_events:
            event_id = unprocessed_event.dictionary_attributes['id']
            created_event_obj = session_get_created_event_by_event_id(
                outer_session=inner_session,
                network_id=network_obj.id,
                event_id=event_id            
            )

            session_update_created_event(
                outer_session=inner_session, 
                event_id=event_id,
                update_vals={
                    'tickets_left': created_event_obj.tickets_total - unprocessed_event.dictionary_attributes['value']
                }
            )
            session_add_new_ticket_minted(
                outer_session=inner_session,
                event_id=event_id,
                amount=unprocessed_event.dictionary_attributes['value'],
                buyer=unprocessed_event.dictionary_attributes['to'],
                indexed_chain_event_id=unprocessed_event.id,
                network_id=network_obj.id,
                tx_hash=unprocessed_event.tx_hash
            )
            
            session_set_event_as_complete(
                outer_session=inner_session, 
                unprocessed_event_id=unprocessed_event.id
            )

    inner_session.close()
