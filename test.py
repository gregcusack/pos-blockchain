
blockchain = Blockchain()
pool = TransactionPool()

alice = Wallet()
bob = Wallet()
exchange = Wallet()
forger = Wallet()

exchangeTransaction = exchange.createTransaction(alice.publicKeyString(), 10, 'EXCHANGE')

if not pool.transactionExists(exchangeTransaction):
    pool.addTransaction(exchangeTransaction)

coveredTransaction = blockchain.getCoveredTransactionSet(pool.transactions)
lastHash = BlockchainUtils.hash_(blockchain.blocks[-1].payload()).hexdigest()
blockCount = blockchain.blocks[-1].blockCount + 1
blockOne = forger.createBlock(coveredTransaction, lastHash, blockCount)
blockchain.addBlock(blockOne) #executes all txs in pool and adds block
pool.removeFromPool(blockOne.transactions)

# alice wants to send 5 tokens to bob
transaction = alice.createTransaction(bob.publicKeyString(), 5, "TRANSFER")

if not pool.transactionExists(transaction):
    pool.addTransaction(transaction)

coveredTransaction = blockchain.getCoveredTransactionSet(pool.transactions)
lastHash = BlockchainUtils.hash_(blockchain.blocks[-1].payload()).hexdigest()
blockCount = blockchain.blocks[-1].blockCount + 1
blockTwo = forger.createBlock(coveredTransaction, lastHash, blockCount)
blockchain.addBlock(blockTwo)  # executes all txs in pool and adds block
pool.removeFromPool(blockTwo.transactions)

pprint.pprint(blockchain.toJson())
