import json

from project.core.decorators.api_gateway_handler import api_gateway_handler
from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.core.helpers.utils import get_from_query_params
from project.core.helpers.validation import is_empty
from project.db.index_chain_event import session_get_latest_event_scanned_by_network
from project.core.session import get_session

logger = get_logger()


@api_gateway_handler
@fname
def latest_event_scanned(event, context):
    network_id = get_from_query_params(event=event, param="network_id")

    if network_id is None:
        raise Exception("No network provided")

    inner_session = get_session(connection_type="readonly")

    res = None

    latest_event_obj = session_get_latest_event_scanned_by_network(outer_session=inner_session, network_id=int(network_id))
    if not is_empty(obj=latest_event_obj):
        res = latest_event_obj.as_dict()

    inner_session.close()

    return res
