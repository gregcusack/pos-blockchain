from Wallet import Wallet
from BlockchainUtils import BlockchainUtils
import requests


def postTransaction(sender, receiver, amount, txType):
    transaction = sender.createTransaction(receiver.publicKeyString(), amount, txType) # fund alice's account
    url = 'http://localhost:5000/transaction'
    package = {'transaction': BlockchainUtils.encode(transaction)}
    request = requests.post(url, json=package)


if __name__ == "__main__":

    bob = Wallet()
    alice = Wallet()
    alice.fromKey('keys/stakerPrivateKey.pem')
    exchange = Wallet()

    # forger: genesis
    postTransaction(exchange, alice, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 100, 'EXCHANGE')
    postTransaction(exchange, bob, 10, 'EXCHANGE')

    # forger: probable alice
    postTransaction(alice, alice, 25, 'STAKE')
    postTransaction(alice, bob, 100, 'TRANSFER')
    postTransaction(alice, bob, 1, 'TRANSFER')



