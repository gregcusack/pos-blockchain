from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from Node import Node
import pprint
import sys


if __name__ == "__main__":

    if len(sys.argv) < 4:
        print("need more args")
    ip = sys.argv[1]
    port = int(sys.argv[2])
    apiPort = int(sys.argv[3])

    node = Node(ip, port)
    node.startP2P()
    node.startAPI(apiPort)

