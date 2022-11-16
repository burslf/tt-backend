import os
from typing import Dict, List

from hexbytes import HexBytes
from web3 import Web3

from project.contracts.abis.billeterie_abi import billeterie_abi
from project.core.helpers.custom_log import get_logger
from project.core.session import get_session
from project.core.web3.web3_helpers import get_web3_instance
from project.db.models import Network
from project.db.network import session_get_networks, network_objs_to_dict
from project.general.chains_configs import contract_addresses, operator_addresses
from project.core.decorators.fname import fname

env = os.environ["ENV"]

logger = get_logger()

minimum_gas_per_function = {
    "createTicketing": 500000,
    "mint": 100000
}


@fname
def call_create_ticketing(supply_price_date: List[int], grey_market_allowed: bool, option_fees: int,
                          offchain_data: str, payees: list, shares: list, network_id: int) -> str:
    inner_session = get_session(connection_type="readonly")

    network_objs: List[Network] = session_get_networks(outer_session=inner_session)
    network_dict: Dict[int, Network] = network_objs_to_dict(network_objs=network_objs)

    network_name = network_dict[network_id].name

    web3 = get_web3_instance(rpc_url=network_dict[network_id].rpc_url)

    billeterie_address = Web3.toChecksumAddress(contract_addresses["billeterie"][env][network_name])

    conditional_fields = [supply_price_date, grey_market_allowed, option_fees, offchain_data, payees, shares]

    if None in conditional_fields:
        raise Exception(f"Missing required field(s)")

    function_args = (supply_price_date, grey_market_allowed, option_fees, offchain_data, payees, shares)

    minimum_gas = minimum_gas_per_function["createTicketing"]

    contract_instance = web3.eth.contract(address=billeterie_address, abi=billeterie_abi)

    nonce = web3.eth.get_transaction_count("0x102BB817B5Acd75d3066B20883a2F917C5677777")

    dict_tx = contract_instance.functions["createTicketing"](*function_args).build_transaction()
    dict_tx["gas"] = minimum_gas
    dict_tx["nonce"] = nonce

    signed_tx = web3.eth.account.sign_transaction(dict_tx, os.environ["PK"])
    raw_tx = signed_tx.rawTransaction
    tx_hash = web3.eth.send_raw_transaction(raw_tx)

    return HexBytes(tx_hash).hex()


@fname
def call_mint(to_address: str, creator: str, event_id: int, amount: int, data: str,
              value: int, network_id: int) -> str:
    inner_session = get_session(connection_type="readonly")

    network_objs: List[Network] = session_get_networks(outer_session=inner_session)
    network_dict: Dict[int, Network] = network_objs_to_dict(network_objs=network_objs)

    network_name = network_dict[network_id].name

    web3 = get_web3_instance(rpc_url=network_dict[network_id].rpc_url)

    billeterie_address = Web3.toChecksumAddress(contract_addresses["billeterie"][env][network_name])

    conditional_fields = [to_address, creator, event_id, amount, data]

    if None in conditional_fields:
        raise Exception(f"Missing required field(s)")

    function_args = (to_address, creator, event_id, amount, data)

    minimum_gas = minimum_gas_per_function["mint"]

    contract_instance = web3.eth.contract(address=billeterie_address, abi=billeterie_abi)

    nonce = web3.eth.get_transaction_count(operator_addresses[0])

    dict_tx = contract_instance.functions["mint"](*function_args).build_transaction({"value": value})
    dict_tx["gas"] = minimum_gas
    dict_tx["nonce"] = nonce

    signed_tx = web3.eth.account.sign_transaction(dict_tx, os.environ["PK"])
    raw_tx = signed_tx.rawTransaction
    tx_hash = web3.eth.send_raw_transaction(raw_tx)

    return HexBytes(tx_hash).hex()
