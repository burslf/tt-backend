from typing import List
from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.db.models import EventCreated
from sqlalchemy.orm import Session

logger = get_logger()


@fname
def session_add_new_created_event(
    outer_session: Session, 
    tx_hash: str, 
    network_id: int,
    event_id: int, 
    creator: str, 
    tickets_total: int,
    tickets_left: int,
    event_date: int,
    options_fees: int,
    offchain_data: str,
    shares: List,
    grey_market_allowed: bool,
    indexed_chain_event_id,
    price: int
):
                          
    event_created = EventCreated()

    event_created.tx_hash = tx_hash
    event_created.network_id = network_id
    event_created.event_id = event_id
    event_created.creator = creator
    event_created.tickets_total = tickets_total
    event_created.tickets_left = tickets_left
    event_created.event_date = event_date
    event_created.options_fees = options_fees
    event_created.offchain_data = offchain_data
    event_created.shares = shares
    event_created.grey_market_allowed = grey_market_allowed
    event_created.indexed_chain_event_id = indexed_chain_event_id
    event_created.price = price

    outer_session.add(event_created)
    outer_session.commit()

    return event_created