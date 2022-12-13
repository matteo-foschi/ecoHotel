from web3 import Web3
import os

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/ecadd76dd30247b4bf4fd9238723bba2'))
    address = '0x1eBF0B06fc1413E1f0ee99fCb2E7309a849c801a'
    privateKey = '0xa4b878b794b89d7faa244b9b933e7b6c0f41b730f4011f39e3ee955ac4dd041b'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0,'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas=100000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId