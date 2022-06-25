## Swap tokens from pancakeswap with web3.py

import time, json, config, re, time
from web3 import Web3
from web3.exceptions import ContractLogicError, SolidityError


web3 = Web3(Web3.HTTPProvider(config.RPC_URL))


def getGasPrice():
    return web3.eth.gasPrice

def SwapTokens(toBuy, WBNB_Address, TokenToSellAddress, contractPancake, walletAddress, symbol, web3, private_key, amountMinOut = 0):
    toBuyBNBAmount = str(toBuy)
    toBuyBNBAmount = web3.toWei(toBuyBNBAmount, 'ether')

    contractPancake = getContractPancake()
    gasPrice = getGasPrice()
    gasPriceGwei = web3.fromWei(gasPrice, 'gwei')

    current_balance = web3.eth.get_balance(walletAddress)
    current_balance_h = web3.fromWei(current_balance, "ether")
    print(f"You have: {current_balance_h} BNB, {float(current_balance_h) - config.amount_left_for_gas} BNB for buy")

    pancakeSwap_txn = contractPancake.functions.swapExactETHForTokens(
        amountMinOut,
        [web3.toChecksumAddress(WBNB_Address), web3.toChecksumAddress(TokenToSellAddress)],
        web3.toChecksumAddress(walletAddress),
        (int(time.time() + 10000))
    ).buildTransaction({
        'from': web3.toChecksumAddress(walletAddress),
        'gasPrice': gasPrice,
        'nonce': web3.eth.get_transaction_count(web3.toChecksumAddress(walletAddress)),
        'value': current_balance - web3.toWei(config.amount_left_for_gas, "ether"),
    })


    try:
        gasLimit = web3.eth.estimate_gas(pancakeSwap_txn)
    except ContractLogicError as error:
        print("ERROR: ", str(error))
        return "Failed At Estimation"

    tx_fees = gasLimit * gasPrice
    pancakeSwap_txn['gas'] = int(gasLimit  + (gasLimit * 0.1))
    print(f"Approx Transaction Fees: {tx_fees / 10 ** 18} BNB With Gwei: {gasPriceGwei}, gasLimit: {int(gasLimit  + (gasLimit * 0.1))}")

    signed_txn = web3.eth.account.sign_transaction(pancakeSwap_txn, private_key=private_key)
    tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_token)
    status = receipt["status"]

    if status == 1:
        print(f"Transaction Hash: {web3.toHex(tx_token)}, Status: {status}", end="\n\n")
        return 'Success'
    else:
        print('Failed')
        return "Failed After broadcasting"
