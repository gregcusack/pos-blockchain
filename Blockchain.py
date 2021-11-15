from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel

# TODO: do we need to take into account a fork in a chain?
class Blockchain:

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()

    def addBlock(self, block):
        self.executeTransactions(block.transactions)
        self.blocks.append(block)

    def toJson(self):
        data = {}
        jsonBlocks = []
        for block in self.blocks:
            jsonBlocks.append(block.toJson())
        data['blocks'] = jsonBlocks
        return data

    def blockCountValid(self, block): # new block to be added to BC
        if self.blocks[-1].blockCount == block.blockCount - 1:
            return True
        return False

    def lastBlockHashValid(self, block):
        latestBlockchainBlockHash = BlockchainUtils.hash_(self.blocks[-1].payload()).hexdigest()
        if latestBlockchainBlockHash == block.lastHash:
            return True
        return False

    def getCoveredTransactionSet(self, transactions):
        coveredTransactions = []
        for transaction in transactions:
            if self.transactionCovered(transaction):
                coveredTransactions.append(transaction)
            else:
                print('Transaction is not covered by sender')
        return coveredTransactions

    def transactionCovered(self, transaction):
        if transaction.type == 'EXCHANGE': # TODO: i think this is just for demo./test purposes. security issue here maybe. just set tx as exchange and automatically works
            return True
        senderBalance = self.accountModel.getBalance(transaction.senderPublicKey)
        if senderBalance >= transaction.amount:
            return True
        return False

    def executeTransactions(self, transactions):
        for transaction in transactions:
            self.executeTransaction(transaction)

    def executeTransaction(self, transaction):
        sender = transaction.senderPublicKey
        receiver = transaction.receiverPublicKey
        amount = transaction.amount
        self.accountModel.updateBalance(sender, -amount)
        self.accountModel.updateBalance(receiver, amount)
