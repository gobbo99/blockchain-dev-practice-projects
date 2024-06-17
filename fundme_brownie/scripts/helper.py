from brownie import network, accounts, config


def get_account():
    print(config["wallets"]["from_key"])
    if network.show_active() == "development":
        acc = accounts[0]
    else:
        acc = accounts.add(config["wallets"]["from_key"])
    return acc
