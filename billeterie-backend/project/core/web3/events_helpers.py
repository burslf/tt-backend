from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.core.web3.web3_helpers import get_block_epochs
from web3 import Web3
from web3._utils.events import get_event_data
from web3._utils.filters import construct_event_filter_params
from hexbytes import HexBytes

logger = get_logger()

@fname
def fetch_event_by_event_name(web3: Web3, event_name: str, from_block: int, to_block: int, address: str, abi: str):
    checksum_address = web3.toChecksumAddress(address)

    contract_instance = web3.eth.contract(address=checksum_address, abi=abi)
    event = getattr(contract_instance.events, event_name)

    abi = event._get_event_abi()
    abi_codec = event.web3.codec

    argument_filters = dict()
    _filters = dict(**argument_filters)

    data_filter_set, event_filter_params = construct_event_filter_params(
        abi,
        abi_codec,
        contract_address=event.address,
        argument_filters=_filters,
        fromBlock=from_block,
        toBlock=to_block,
        address=checksum_address,
    )

    logs = event.web3.eth.getLogs(event_filter_params)

    for entry in logs:
        data = get_event_data(abi_codec, abi, entry)
        yield data


@fname
def get_all_latest_events(web3: Web3, from_block: int, network_name: str, event_name: str,
                          contract_address: str, abi: str):
    res = []

    block_epochs = get_block_epochs(web3=web3, from_block=from_block, network_name=network_name)

    for epoch in block_epochs:
        res_events = fetch_event_by_event_name(web3=web3,
                                               event_name=event_name,
                                               from_block=epoch["from_block"],
                                               to_block=epoch["to_block"],
                                               address=contract_address,
                                               abi=abi)
        res_events_list = list(res_events)

        for event in res_events_list:
            new_event = {
                "event_name": event.event,
                "args": dict(event.args),
                "block_number": event.blockNumber,
                "tx_hash": HexBytes(event.transactionHash).hex()
            }
            res.append(new_event)

    return res
