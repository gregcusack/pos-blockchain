from Transaction import Transaction
from Wallet import Wallet
from TransactionPool import TransactionPool
from Block import Block
from Blockchain import Blockchain
from BlockchainUtils import BlockchainUtils
import pprint


if __name__ == "__main__":
    sender = 'sender'
    receiver = 'receiver'
    amount = 1
    type = 'TRANSFER'

    # transaction = Transaction(sender, receiver, amount, type)
    # wallet = Wallet()
    # signature = wallet.sign(transaction.toJson())   # sign the transaction
    # transaction.sign(signature)
    # signatureValid = Wallet.signatureValid(transaction.payload(), signature, wallet.publicKeyString())
    # print(signatureValid)

    wallet = Wallet()
    fraudulentWallet = Wallet()
    pool = TransactionPool()
    transaction = wallet.createTransaction(receiver, amount, type)

    if pool.transactionExists(transaction) == False:
        pool.addTransaction(transaction)

    blockchain = Blockchain()

    lastHash = BlockchainUtils.hash_(blockchain.blocks[-1].payload()).hexdigest()
    blockCount = blockchain.blocks[-1].blockCount + 1
    block = wallet.createBlock(pool.transactions, lastHash, blockCount)
    # signatureValid = Wallet.signatureValid(block.payload(), block.signature, wallet.publicKeyString())

    if not blockchain.lastBlockHashValid(block):
        print('lastBlockHash is not valid')
    if not blockchain.blockCountValid(block):
        print('Blockcount is not valid')

    if blockchain.lastBlockHashValid(block) and blockchain.blockCountValid(block):
        blockchain.addBlock(block)

    # blockchain.addBlock(block)
    pprint.pprint(blockchain.toJson())

