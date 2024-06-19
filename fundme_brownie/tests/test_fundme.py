import pytest
from brownie import FundMe, network, accounts, exceptions
from scripts.deploy import  deploy_fund_me
from scripts.helper import LOCAL_BLOCKCHAIN_ENVIRONMENTS, FORKED_ENVIRONMENTS, get_account


"""
Functions must start with 'test'
"""


def test_can_fund_withdraw():
    fund_me = deploy_fund_me()
    acc = get_account()
    entrance_fee = fund_me.getEntranceFee() + 100
    tx1 = fund_me.fund({"from": acc, "value": entrance_fee})
    tx1.wait(1)
    assert fund_me.addressAmountMapping(acc.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": acc})
    tx2.wait(1)
    assert fund_me.addressAmountMapping(acc.address) == 0


def test_only_owner_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    bad_actor = accounts.add()
    fund_me.withdraw({"from": bad_actor.address})
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
