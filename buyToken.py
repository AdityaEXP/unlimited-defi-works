from web3 import Web3
import json, os, re


class config:
  CONTRACT_PANCAKE = "" #Router address
  WBNB_ADDRESS = "" #Address of the main token bnb, eth 

  
def getContractPancake():
    with open(os.getcwd().replace('\\', '/') + '/ABI/router.json', 'r') as file: abi = json.load(file) #ABI are in main file
    contractPancake = web3.eth.contract(address=web3.toChecksumAddress(config.CONTRACT_PANCAKE), abi=abi)
    return contractPancake

def getAmountsOut(base_address, token_address, base_amount):
    """
    :base_address: WBNB or something
    :token_address: buying token
    :base_amount: in wei
    
    """

    contractPancake = getContractPancake()

    result = contractPancake.functions.getAmountsOut(
        int(base_amount),
        [ web3.toChecksumAddress(base_address), web3.toChecksumAddress(token_address) ]
    ).call()

    return result[1]
  
  def buyWithSlippageProtection(amount_bnb, receipt_address, target_token_address, slippage):
    """
    amount_bnb: 0.001
    receipt_address: 0xxxxx
    target_token_address: 0xxxxx
    slippage: 0.15%, 0.5%
    """

    result = getAmountsOut(
        config.WBNB_ADDRESS,
        web3.toChecksumAddress(target_token_address),
        amount_bnb * 10 ** 18
    )
    slippageAmount = result - (result * (slippage))
    swap_func = contract.functions.swapExactETHForTokens(
        int(slippageAmount),
        [config.WBNB_ADDRESS, target_token_address],
        web3.toChecksumAddress(receipt_address),
        int(time.time() + 1000000000)
    )

    return swap_func
  
from seatrader import config
from seatrader.utils.web3Provider import getAmountsOut, roundToNearestZero
from web3 import Web3
import time, os, json


web3 = Web3(Web3.HTTPProvider(config.RPC_URL))
with open(os.getcwd().replace('\\', '/') + '/seatrader/ABI/router.json', 'r') as file: abiRouter = json.load(file)
contract = web3.eth.contract(address=config.CONTRACT_PANCAKE, abi=abiRouter)


def buyWithSlippageProtection(amount_bnb, receipt_address, target_token_address, slippage):
    """
    amount_bnb: 0.001
    receipt_address: 0xxxxx
    target_token_address: 0xxxxx
    slippage: 0.15%, 0.5%
    """

    result = getAmountsOut(
        config.WBNB_ADDRESS,
        web3.toChecksumAddress(target_token_address),
        amount_bnb * 10 ** 18
    )
    slippageAmount = result - (result * (slippage))
    swap_func = contract.functions.swapExactETHForTokens(
        int(slippageAmount),
        [config.WBNB_ADDRESS, target_token_address],
        web3.toChecksumAddress(receipt_address),
        int(time.time() + 1000000000)
    )

    return swap_func



PRIVATE_KEY = '0xxxxxxxxxxxxxx'
AMOUNT = 0.1
DECIMAL_TOKEN = 18
TOKEN_ADDRESS = web3.toChecksumAddress('0x17e65e6b9b166fb8e7c59432f0db126711246bc0')
SLIPPAGE = 0.15 #15%


swap_func = buyWithSlippageProtection(
    amount_bnb=AMOUNT,
    receipt_address=web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
    target_token_address=TOKEN_ADDRESS,
    slippage=SLIPPAGE
)

tx = swap_func.buildTransaction({
    "from": web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
    "chainId": web3.eth.chain_id,
    "gasPrice": web3.eth.gas_price,
    "value": int(AMOUNT * 10 ** DECIMAL_TOKEN),
    "gas": 0
})

tx['gas'] = web3.eth.estimate_gas(tx)
tx['nonce'] = web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address)

signedTx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
broadcastedTx = web3.eth.send_raw_transaction(signedTx.rawTransaction)
result = web3.eth.wait_for_transaction_receipt(broadcastedTx)

print(result)


  
  
