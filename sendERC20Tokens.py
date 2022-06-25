import time, json, re, time
from web3 import Web3
from web3.exceptions import ContractLogicError, SolidityError

RPC_URL = ""
CHAIN_ID = ""
web3 = Web3(Web3.HTTPProvider(RPC_URL))


def sendTokenFromWallet(from_add, to_add, token_contract, private_key):
    with open('./ABI/basic.json', 'r') as file: abiData = json.load(file)
    contract = web3.eth.contract(address=web3.toChecksumAddress(token_contract), abi=abiData)

    decimal = contract.functions.decimals().call()
    avail_amount = contract.functions.balanceOf(from_add).call() / 10 ** int(decimal)
    gasPrice = web3.eth.gas_price

    print(f"Wallet: {from_add}, Tokens: {avail_amount}")

    tx = contract.functions.transfer(
        web3.toChecksumAddress(to_add),
        int(avail_amount * 10 ** decimal)
    ).buildTransaction({
        "chainId": int(CHAIN_ID),
        'from': from_add,
        'gasPrice': gasPrice,
        'nonce': web3.eth.getTransactionCount(from_add)
    })

    gasLimit = web3.eth.estimate_gas(tx)
    tx['gas'] = gasLimit

    signed_txn = web3.eth.account.sign_transaction(tx, private_key=private_key)


    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_token)
    status = receipt["status"]

    if status == 1:
        print(f"Transaction Hash: {web3.toHex(tx_token)}, Status: {status}", end="\n\n")
    else:
        print('Failed')
        return "Failed"
