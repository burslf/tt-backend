from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.db.models import IndexedChainEvent
from sqlalchemy.orm import Session

logger = get_logger()


@fname
def session_add_new_event(outer_session: Session, event_name: str, contract_address: str, dict_attr: dict,
                          block_number: int, tx_hash: str, network_id: int):
    indexed_chain_event = IndexedChainEvent()

    indexed_chain_event.event_name = event_name
    indexed_chain_event.contract_address = contract_address
    indexed_chain_event.dictionary_attributes = dict_attr
    indexed_chain_event.block_number = block_number
    indexed_chain_event.tx_hash = tx_hash
    indexed_chain_event.network_id = network_id

    outer_session.add(indexed_chain_event)
    outer_session.commit()

    return indexed_chain_event


@fname
def session_get_latest_event_scanned_by_network(outer_session: Session, network_id: int) -> IndexedChainEvent:
    conditional_fields = [outer_session, network_id]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = (outer_session.query(IndexedChainEvent)
           .filter(IndexedChainEvent.network_id == network_id)
           .order_by(IndexedChainEvent.block_number.desc())
           .first()
           )

    return res


@fname
def session_get_latest_event_scanned_by_event_and_network(outer_session: Session, event_name: str,
                                                          network_id: int) -> IndexedChainEvent:
    conditional_fields = [outer_session, event_name, network_id]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = (outer_session.query(IndexedChainEvent)
           .filter(IndexedChainEvent.network_id == network_id)
           .filter(IndexedChainEvent.event_name == event_name)
           .order_by(IndexedChainEvent.block_number.desc())
           .first()
           )

    return res


@fname
def session_get_all_events_by_network(outer_session: Session, network_id:int) -> [IndexedChainEvent]:
    conditional_fields = [outer_session, network_id]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = (outer_session.query(IndexedChainEvent)
           .filter(IndexedChainEvent.network_id == network_id)
           .all()
           )

    return res

