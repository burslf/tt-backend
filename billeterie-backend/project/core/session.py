import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.pool import NullPool


def get_connection_string(connection_type: str):
    valid_connection_types = ["readonly", "readwrite"]

    connection_string = os.getenv("DATABASE_URL")

    return connection_string


def get_session(connection_type: str) -> Session:
    connection_string = get_connection_string(connection_type=connection_type)

    engine = create_engine(connection_string, poolclass=NullPool, pool_pre_ping=True)

    Session = sessionmaker(bind=engine, expire_on_commit=False)
    session = Session()

    return session
