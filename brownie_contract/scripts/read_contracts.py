from brownie import MemeContract, accounts, config
"""
We can access previous deployments
    for i in range(len(MemeContract)):
        print(f"{i}. - ", end="")
        print(MemeContract[i])
"""


def read_contract():
    for i in range(len(MemeContract)):
        meme_contract = MemeContract[i]
        print(meme_contract.getFavMeme())


def main():
    read_contract()
