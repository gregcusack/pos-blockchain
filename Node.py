from TransactionPool import TransactionPool
from Wallet import Wallet
from Blockchain import Blockchain
from SocketCommunication import SocketCommunication
from NodeAPI import NodeAPI


class Node:

    def __init__(self, ip, port):
        self.p2p = None
        self.ip = ip
        self.port = port
        self.transactionPool = TransactionPool()
        self.wallet = Wallet()
        self.blockchain = Blockchain()

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication()

    def startAPI(self, apiPort):
        self.api = NodeAPI()
        self.api.injectNode(self)
        self.api.start(apiPort)

    """
    1) check if tx is valiud (check signature
    2) make sure transaction not already in tx pool
    @note: need 3 things to validate signature
        1) data which was initially used to create signature
        2) signature
        3) signers public key
    """
    def handleTransaction(self, transaction):
        data = transaction.payload()
        signature = transaction.signature
        signersPublicKey = transaction.senderPublicKey
        signatureValid = Wallet.signatureValid(data, signature, signersPublicKey)
        transactionExists = self.transactionPool.transactionExists(transaction)
        if not transactionExists and signatureValid:
            self.transactionPool.addTransaction(transaction)