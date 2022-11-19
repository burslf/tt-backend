import json
from typing import List

from project.db.models import EventCreated

from project.core.decorators.api_gateway_handler import api_gateway_handler
from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.core.helpers.utils import get_from_query_params
from project.core.helpers.validation import is_empty
from project.db.event_created import session_get_created_events
from project.core.session import get_session

logger = get_logger()


@api_gateway_handler
@fname
def api_get_created_events(event, context):
    network_id = get_from_query_params(event=event, param="network_id")

    if network_id is None:
        raise Exception("No network provided")

    inner_session = get_session(connection_type="readonly")

    res = []

    created_event_objs: List[EventCreated] = session_get_created_events(outer_session=inner_session, network_id=int(network_id))
    
    inner_session.close()

    res = [e.as_dict() for e in created_event_objs]

    return res
