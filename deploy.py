#  yarn global add ganache-cli
#  yarn global bin, yarn config set prefix..
#  deployment using web3.py and py-solc-x libraries
import json
import pprint
from dotenv import load_dotenv
import os
from solcx import compile_standard, install_solc
from web3 import Web3


load_dotenv()

with open('contracts1/MemeContract.sol', 'r') as f:
    raw_contract = f.read()

install_solc(version="latest")

# Compile solidity code
compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"MemeContract.sol": {"content": raw_contract}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}
            }
        }
    },
    solc_version="0.8.16"
)

# get bytecode and abi of contract
bytecode = compiled["contracts"]["MemeContract.sol"]["MemeContract"]["evm"]["bytecode"]["object"]
abi = compiled["contracts"]["MemeContract.sol"]["MemeContract"]["abi"]

chain_id = 11155111
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/92d2cb193fbd444e91175acf4e61d54c"))  #

addr = "0xF41D401bA4E55C21b216923f0638bf40aDEC436D"  # metamask 4fun sepolia eth addr

meme_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.get_transaction_count(addr)

#  1. Build a transaction
#  2. Sign a transaction
#  3. Send a transaction and wait confirmation
transaction = meme_contract.constructor().build_transaction({"chainId": chain_id, "from": addr, "nonce": nonce, "gasPrice": w3.eth.gas_price})
signed_tx = w3.eth.account.sign_transaction(transaction, private_key=os.getenv("PKEY"))
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
deployed_contract = w3.eth.contract(abi=abi, address=tx_receipt.contractAddress)
print("Deployed!")

tx2 = deployed_contract.functions.addSubject("Fifi", 150, True).build_transaction(
    {
        "chainId": chain_id,
        "nonce": nonce + 1,
        "from": addr,
        "gasPrice": w3.eth.gas_price,
        # "gas": 2000000,
        # "gasPrice": 2000000,
    }
)
signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key=os.getenv("PKEY"))
print("Updating contract...")
tx_hash = w3.eth.send_raw_transaction(signed_tx2.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Updated!")

# Working with contract we need address + contract ABI
# meme_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call - no state change   Transact - state change
print(deployed_contract.functions.showAll().call())

