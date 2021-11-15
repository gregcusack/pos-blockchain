
class TransactionPool:

    def __init__(self):
        self.transactions = []

    def addTransaction(self, transaction):
        self.transactions.append(transaction)

    # TODO: this is extremely slow. we should use a hash map or binary tree
    def transactionExists(self, transaction):
        # check if transaction already exists in pool
        for poolTransaction in self.transactions:
            if poolTransaction.equals(transaction):
                return True
        return False

    # remove txs from pool that are going into next block
    def removeFromPool(self, transactions):
        newPoolTransactions = []
        for poolTransaction in self.transactions:
            insert = True
            for transaction in transactions:
                if poolTransaction.equals(transaction):
                    insert = False # don't insert into new list
            if insert:
                newPoolTransactions.append(poolTransaction)
        self.transactions = newPoolTransactions

