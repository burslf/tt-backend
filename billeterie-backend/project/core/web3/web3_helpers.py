import os
import time

from web3 import Web3
from web3.middleware import geth_poa_middleware

from project.core.decorators.fname import fname
from project.core.helpers.custom_log import get_logger
from project.general.chains_configs import block_interval_per_chain

env = os.environ["ENV"]

logger = get_logger()


@fname
def get_web3_instance(rpc_url: str, n_attempts: int = 7):
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    attempt = 0

    connected = False
    while not connected and attempt < n_attempts:
        logger.info(f"Attempt number #{attempt}")
        connected = web3.isConnected()
        if not connected:
            error_message = f"RPC url - {rpc_url} - not able to connect"

            logger.error(error_message)
            attempt += 1
            time.sleep(1)

    if not connected:
        raise Exception("Could not connect to rpc ")

    logger.info(f"Web3 connected == {connected}")

    return web3


@fname
def get_block_epochs(web3: Web3, from_block: int, network_name: str):
    latest_block = web3.eth.get_block_number()
    block_counter = from_block

    epochs = []
    block_interval = block_interval_per_chain[env][network_name]

    while (block_counter + block_interval) < latest_block:
        epochs.append({
            "from_block": block_counter,
            "to_block": block_counter + block_interval
        })
        block_counter += block_interval

    epochs.append({
        "from_block": block_counter,
        "to_block": latest_block
    })

    return epochs
