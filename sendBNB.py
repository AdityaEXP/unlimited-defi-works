import time, json, config, re, time
from web3 import Web3
from web3.exceptions import ContractLogicError, SolidityError

RPC_URL = ""
CHAIN_ID = ""
web3 = Web3(Web3.HTTPProvider(RPC_URL))

def sendBNB(from_add, to_add, private_key):
    GasPrice = web3.eth.gasPrice

    tx = {
        'chainId': int(CHAIN_ID),
        'from': web3.toChecksumAddress(from_add),
        'to': web3.toChecksumAddress(to_add),
        'nonce': web3.eth.getTransactionCount(web3.toChecksumAddress(from_add)),
        'gasPrice': GasPrice,
        "gas": 0
    }

    gasLimit = web3.eth.estimate_gas(tx)
    transactionFees = GasPrice * gasLimit

    tx['gas'] = gasLimit
    tx['value'] = web3.eth.getBalance(from_add) - transactionFees

    signed_txn = web3.eth.account.sign_transaction(tx, private_key=private_key)


    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_token)
    status = receipt["status"]

    if status == 1:
        print(f"Transaction Hash: {web3.toHex(tx_token)}, Status: {status}", end="\n\n")
    else:
        print('Failed')
        return "Failed"
