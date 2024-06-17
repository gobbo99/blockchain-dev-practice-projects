import os

from brownie import accounts, config, MemeContract, network


"""
# acc = accounts.load("4fun")  # has many methods, attributes --> balance, deploy, estimate_gas, transfer...
Brownie knows if a method is a "call" or "transaction" type, transaction type requires "from" value

"""


def deploy_contract():
    acc = get_account()
    c = MemeContract.deploy({"from": acc})
    transaction = c.setFavMeme("PEPE")
    transaction.wait(1)
    updated_value = c.getFavMeme()
    print(updated_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_contract()