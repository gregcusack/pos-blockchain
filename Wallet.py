from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from BlockchainUtils import BlockchainUtils
from Transaction import Transaction

class Wallet:

    def __init__(self):
        self.keyPair = RSA.generate(2048) #2048 is mod number for RSA

    # takes data and creates signature based on keypair
    def sign(self, data):
        dataHash = BlockchainUtils.hash_(data)
        signatureSchemeObject = PKCS1_v1_5.new(self.keyPair) # scheme object used to sign data. use key pair's priv key
        signature = signatureSchemeObject.sign(dataHash)  # sign input data
        return signature.hex()

    #validate signatures without needing to create instances of wallet class
    @staticmethod
    def signatureValid(data, signature, publicKeyString): #pubkey of wallet used to sign the data
        signature = bytes.fromhex(signature)
        dataHash = BlockchainUtils.hash_(data)
        publicKey = RSA.importKey(publicKeyString) # pubkey is recreated from string representation
        signatureSchemeObject = PKCS1_v1_5.new(publicKey) # now we are validating using public key (we signed using priv key above)
        signatureValid = signatureSchemeObject.verify(dataHash, signature)
        return signatureValid

    # don't have ability to extract pubkey from the self.keypair!
    def publicKeyString(self):
        # public_key() returns key obj. exportKey('PEM') returns binary. decode returns string
        publicKeyString = self.keyPair.public_key().exportKey('PEM').decode('utf-8')
        return publicKeyString

    # sender always owner of wallet
    def createTransaction(self, receiver, amount, type):
        trasaction = Transaction(self.publicKeyString(), receiver, amount, type)
        signature = self.sign(trasaction.payload())
        trasaction.sign(signature)
        return trasaction
