from web3 import Web3

w3 = Web3(Web3.HTTPProvider('https://ropsten.infura.io/v3/afc5e614f3454316a5de4683706ddb01'))
account = w3.eth.account.create()
privateKey = account.privateKey.hex()
address = account.address

print(f"Your addres: {address} \nYour key: {privateKey}")