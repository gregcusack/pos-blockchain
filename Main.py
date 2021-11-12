from Transaction import Transaction
from Wallet import Wallet

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
    transaction = wallet.createTransaction(receiver, amount, type)
    #validate signature
    signatureValid = Wallet.signatureValid(transaction.payload(), transaction.signature, wallet.publicKeyString())
    fraudSignatureValid = Wallet.signatureValid(transaction.payload(), transaction.signature, fraudulentWallet.publicKeyString())

    print(signatureValid)
    print(fraudSignatureValid)