from web3 import Web3
from brownie import network, accounts, config, MockV3Aggregator


DECIMALS = 8
STARTING_PRICE = 2000000000000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ['ganache-local', 'ganache-local-gui', 'development']
FORKED_ENVIRONMENTS = ['mainnet-fork', 'mainnet-fork-dev']


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS or network.show_active() in FORKED_ENVIRONMENTS:
        acc = accounts[0]
    else:
        acc = accounts.add(config["wallets"]["from_key"])
    return acc


"""
Function to deploy mock aggregator price feed object which will act to emulate real mock aggregator but runs locally
If mock aggregator for contract exists, use that one
"""


def deploy_mocks():
    if len(MockV3Aggregator) == 0:
        print("Deploying mock...")
        mock_aggregator = MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
        print("Mocks deployed!")
        return mock_aggregator.address
    else:
        print(f"Using existing mock aggregator: {MockV3Aggregator[-1].address}")
        return MockV3Aggregator[-1].address
