from typing import List
from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.db.models import TicketMinted
from sqlalchemy.orm import Session

logger = get_logger()


@fname
def session_add_new_ticket_minted(
    outer_session: Session, 
    tx_hash: str, 
    network_id: int,
    event_id: int, 
    indexed_chain_event_id,
    buyer: str,
    amount: int
):
                          
    ticket_minted = TicketMinted()

    ticket_minted.tx_hash = tx_hash
    ticket_minted.network_id = network_id
    ticket_minted.indexed_chain_event_id = indexed_chain_event_id
    ticket_minted.event_id = event_id
    ticket_minted.buyer = buyer
    ticket_minted.amount = amount

    outer_session.add(ticket_minted)
    outer_session.commit()

    return ticket_minted

@fname
def session_get_tickets_minted(outer_session: Session, network_id:int) -> List[TicketMinted]:
    conditional_fields = [outer_session, network_id]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = (outer_session.query(TicketMinted)
           .filter(TicketMinted.network_id == network_id)
           .all()
           )

    return res

@fname
def session_get_tickets_minted_by_event_id(outer_session: Session, network_id: int, event_id: int) -> TicketMinted:
    conditional_fields = [outer_session, network_id]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = (outer_session.query(TicketMinted)
           .filter(TicketMinted.network_id == network_id)
           .filter(TicketMinted.event_id == event_id)
           .first()
           )

    return res
