import uuid #creates unique random ids
import time
import copy

class Transaction:

    def __init__(self, senderPublicKey, receiverPublicKey, amount, type):
        self.senderPublicKey = senderPublicKey
        self.receiverPublicKey = receiverPublicKey
        self.amount = amount
        self.type = type
        self.id = uuid.uuid1().hex      # create globally unique id
        self.timestamp = time.time()    # create unix timestamp
        self.signature = ''             # only owner of private key is entitled to create transactions in its name

    def toJson(self):
        return self.__dict__

    def sign(self, signature):
        self.signature = signature

    # tries to generate as tojson but always sets signature to empty payload
    # consistent representation of transaction no matter if it's already been signed or not
    def payload(self):
        jsonRepresentation = copy.deepcopy(self.toJson())
        jsonRepresentation['signature'] = ''
        return jsonRepresentation

    def equals(self, transaction):
        if self.id == transaction.id:
            return True
        return False
