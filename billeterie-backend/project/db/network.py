from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.db.models import Network
from sqlalchemy.orm import Session

logger = get_logger()


@fname
def session_add_new_network(outer_session: Session, network_name: str, block_scanner_url: str, rpc_url: str):
    network = Network()

    network.name = network_name
    network.block_scanner_url = block_scanner_url
    network.rpc_url = rpc_url

    outer_session.add(network)
    outer_session.commit()

    return network


@fname
def session_get_networks(outer_session: Session) -> [Network]:
    conditional_fields = [outer_session]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = outer_session.query(Network).all()

    return res


@fname
def session_get_network_details_by_name(outer_session: Session, network_name: str):
    conditional_fields = [outer_session, network_name]

    if None in conditional_fields:
        raise Exception(f"{fname} conditional_fields: {conditional_fields}")

    res = outer_session.query(Network).filter(Network.name == network_name).first()

    return res


def network_objs_to_dict(network_objs: [Network]) -> dict:
    res = {}

    for network in network_objs:
        res[network.id] = network

    return res
