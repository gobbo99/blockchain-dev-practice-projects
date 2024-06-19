import time

from brownie import accounts, MockV3Aggregator, FundMe, Contract, network, config
from web3 import Web3
from .helper import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    mark = time.time()
    acc = get_account()
    active_network = network.show_active()
    print(f"Network is set to: {active_network}")
    if active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        caddr = deploy_mocks()
    else:
        caddr = config['networks'][active_network]['price_feed']
    fund_me = FundMe.deploy(caddr, {"from": acc}, publish_source=config["networks"][active_network].get("verify"))
    print(f"Fundme contract deployed to {fund_me.address}")
    print(f"\nElapsed: {time.time() - mark}s")
    return fund_me


def publish():
    my_contract = Contract.from_abi("MyContract", "0x9f45af1a8b40b283E7953cEf37EF6E7E33Fb41f9", FundMe.abi)
    res = FundMe.publish_source(my_contract)
    print(res)


def main():
    deploy_fund_me()