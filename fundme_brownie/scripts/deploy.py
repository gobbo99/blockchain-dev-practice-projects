import os
import time
import json

from brownie import accounts, FundMe, Contract, network, config
from .helper import get_account


def deploy_fund_me():
    mark = time.time()
    acc = get_account()
    try:
        fund_me = FundMe.deploy({"from": acc}, publish_source=True)
    except(Exception) as e:
        print(e)
    print(f"\nElapsed: {time.time() - mark}s")


def publish():
    my_contract = Contract.from_abi("MyContract", "0x9f45af1a8b40b283E7953cEf37EF6E7E33Fb41f9", FundMe.abi)
    res = FundMe.publish_source(my_contract)
    print(res)


def main():
    deploy_fund_me()