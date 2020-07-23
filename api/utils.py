from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/afc5e614f3454316a5de4683706ddb01'))
    address = '0x67364b1A23f2bDE1146E584F4fFfD9bF5593D32F'
    privateKey = '0xbae0cbbdbcb3aded2220f3e0168c746473100c4cbc47616f508baa03b5c56395'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0,'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce = nonce,
        gasPrice = gasPrice,
        gas = 100000,
        to = '0x0000000000000000000000000000000000000000',
        value = value,
        data = message.encode('utf-8')
        ), privateKey)
    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId
