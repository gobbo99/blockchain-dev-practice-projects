from brownie import FundMe
from .helper import get_account


def fund():
    fund_me = FundMe[-1]
    acc = get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(f"Current entry fee: {entrance_fee}")
    fund_me.fund({"from": acc, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    acc = get_account()
    fund_me.withdraw({"from": acc})


def main():
    fund()
