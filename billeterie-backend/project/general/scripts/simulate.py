
import logging

from project.db.event_created import session_get_created_events
# import os
from project.core.helpers.load_env import load_environment_variables

import sys

load_environment_variables(env="develop", parent_level=0)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from project.lambdas.event_processors.event_created_processor import event_created_processor

from project.core.session import get_session



import boto3


# from project.core.session import get_session
# from project.db.index_chain_event import session_get_all_events_by_network

# from project.db.network import session_get_networks, session_add_new_network

# from project.core.session import get_session
from project.general.sqs import send_message, get_sqs_message
from project.contracts.function_calls.billeterie import call_mint, call_create_ticketing
# from project.core.helpers.slack_message import send_slack_message
# from project.lambdas.api.web3_instance_api import web3_instance_api
# from modules.web3.web3_helpers import get_web3_instance
# from project.lambdas.monitor.event_monitor import event_monitor
# from project.lambdas.api.latest_event_scanned import latest_event_scanned


# res = call_create_ticketing(supply_price_date=[100, 1000000000000000, 1668608452], 
#                             grey_market_allowed=True,
#                             option_fees=7,
#                             offchain_data="https://y0669s0jj1.execute-api.us-east-1.amazonaws.com/develop/event_uri?token_id=1",
#                             payees=["0x102BB817B5Acd75d3066B20883a2F917C5677777"], 
#                             shares=[100], 
#                             network_id=1
# )

# res = call_mint(to_address="0x102BB817B5Acd75d3066B20883a2F917C5677777",
#                 creator="0x102BB817B5Acd75d3066B20883a2F917C5677777", 
#                 amount=2, 
#                 event_id=1, 
#                 data="0x",
#                 value=2000000000000000, 
#                 network_id=1
# )

# print(res)

# res = event_monitor(event={"network_id": 1}, context={})
# res = latest_event_scanned(event={"queryStringParameters": {"network_id":1}}, context={})
# res = web3_instance_api(event={"queryStringParameters":{"network_id":1}}, context={})


# res = send_slack_message(mentions=["Yoel"], message="TEST", channel="alert-test", color="fcba03")

# res = session_add_new_network(outer_session=inner_sess, network_name="RINKEBY",
#                               block_scanner_url="https://rinkeby.etherscan.io", rpc_url="https://rinkeby.infura.io/v3/d53260b9f071444bab2b519f2a52b1a8")

# message = get_sqs_message(function_name="activity_monitor", message_body={})
# print(message)
# send_message(queue_name="activity_monitor", messages=[message])

inner_session = get_session(connection_type="readonly")

res = session_get_created_events(outer_session=inner_session, network_id=1)
# res = event_created_processor(event={}, context={})
print(res)