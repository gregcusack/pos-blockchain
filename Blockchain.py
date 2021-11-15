from Block import Block
from BlockchainUtils import BlockchainUtils
from AccountModel import AccountModel
from ProofOfStake import ProofOfStake


# TODO: do we need to take into account a fork in a chain?
# TODO: bug. duplicate blocks. blocks added to chain even if no transaction. happens when invalid transaction submitted
class Blockchain:

    def __init__(self):
        self.blocks = [Block.genesis()]
        self.accountModel = AccountModel()
        self.pos = ProofOfStake()

    # todo: bug here maybe? blocks getting added twice
    def addBlock(self, block):
        # self.executeTransactions(block.transactions)
        # self.blocks.append(block)
        if self.blocks[-1].blockCount < block.blockCount:
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
        # enforce that the wallet owner is only able to stake for themselves. bob cannot stake for alice
        if transaction.type == 'STAKE':
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            if sender == receiver:
                amount = transaction.amount
                self.pos.update(sender, amount)
                self.accountModel.updateBalance(sender, -amount) # we stake tokens so they need to be removed from our account
        else:
            sender = transaction.senderPublicKey
            receiver = transaction.receiverPublicKey
            amount = transaction.amount
            self.accountModel.updateBalance(sender, -amount) # update balance using negative number here is weird
            self.accountModel.updateBalance(receiver, amount)

    def nextForger(self):
        lastBlockHash = BlockchainUtils.hash_(self.blocks[-1].payload()).hexdigest()
        nextForger = self.pos.forger(lastBlockHash)
        return nextForger

    def createBlock(self, transactionFromPool, forgerWallet):
        coveredTransactions = self.getCoveredTransactionSet(transactionFromPool)
        self.executeTransactions(coveredTransactions)
        newBlock = forgerWallet.createBlock(coveredTransactions,
                                            BlockchainUtils.hash_(self.blocks[-1].payload()).hexdigest(),
                                            len(self.blocks))
        self.blocks.append(newBlock)
        return newBlock

    # need to check to make sure a tx we receive has not already been executed and is on blockchain
    def transactionExists(self, transaction):
        for block in self.blocks:
            for blockTransaction in block.transactions:
                if transaction.equals(blockTransaction):
                    return True # tx already in blockchain. need to ignore
        return False

    def forgerValid(self, block):
        forgerPublicKey = self.pos.forger(block.lastHash)
        proposedBlockForger = block.forger
        if forgerPublicKey == proposedBlockForger:
            return True
        return False

    def transactionValid(self, transactions):
        coveredTransactions = self.getCoveredTransactionSet(transactions)
        if len(coveredTransactions) == len(transactions):
            return True
        return False
