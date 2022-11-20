# import uuid
# from modules.helpers.helpers import get_time_now
import json
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, UniqueConstraint, JSON, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def transform_to_dict(model):
    res = {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return json.loads(json.dumps(res, default=str))


class IndexedChainEvent(Base):
    __tablename__ = "indexed_chain_event"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    event_name = Column(String(200), nullable=False)
    contract_address = Column(String(200), nullable=False)
    dictionary_attributes = Column(JSON, nullable=False)
    block_number = Column(Integer, nullable=False)
    tx_hash = Column(String(200), nullable=False)
    network_id = Column(Integer, ForeignKey("network.id"), nullable=False)
    completed = Column(Boolean, default=False, server_default="False", nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "contract_address", "event_name", "network_id", "tx_hash", name="uc_contract_event_name_network_id_tx_hash"
        ),
    )

    def as_dict(self):
        return transform_to_dict(model=self)


class Network(Base):
    __tablename__ = "network"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    name = Column(String(200), nullable=False)
    block_scanner_url = Column(String(200), nullable=False)
    rpc_url = Column(String(200), nullable=False)
    __table_args__ = (
        UniqueConstraint(
            "name", "block_scanner_url", name="uc_contract_name_block_scanner_url"
        ),
    )

    def as_dict(self):
        return transform_to_dict(model=self)

class EventCreated(Base):
    __tablename__ = "event_created"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    tx_hash = Column(String(200), nullable=False)
    indexed_chain_event_id = Column(Integer, ForeignKey("indexed_chain_event.id"), nullable=False)
    event_id = Column(Integer, nullable=False)
    creator = Column(String(200), nullable=False)
    tickets_total = Column(Integer, nullable=False)
    tickets_left = Column(Integer, nullable=False, default=False)
    price = Column(Integer, nullable=False)
    event_date = Column(Integer, nullable=False)
    options_fees = Column(Integer, nullable=False)
    offchain_data = Column(String(200))
    shares = Column(JSON)
    grey_market_allowed = Column(Boolean, default=False, server_default="False", nullable=False)
    network_id = Column(Integer, ForeignKey("network.id"), nullable=False)
    
    __table_args__ = (
        UniqueConstraint(
            "event_id", name="uc_event_id"
        ),
    )

    def as_dict(self):
        return transform_to_dict(model=self)

class TicketMinted(Base):
    __tablename__ = "ticket_minted"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), onupdate=datetime.utcnow)
    tx_hash = Column(String(200), nullable=False)
    network_id = Column(Integer, ForeignKey("network.id"), nullable=False)
    indexed_chain_event_id = Column(Integer, ForeignKey("indexed_chain_event.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event_created.event_id"), nullable=False)
    buyer = Column(String(200), nullable=False)
    amount = Column(Integer, nullable=False)

    __table_args__ = (

    )

    def as_dict(self):
        return transform_to_dict(model=self)
