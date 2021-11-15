# BlockchainUtils.py
# methods used across whole application
from Crypto.Hash import SHA256
import json
import jsonpickle


class BlockchainUtils:

    # static methods and don't have to create instance of BlockchainUtils to use
    @staticmethod
    def hash_(data):
        # don't know type of data. could be obj, dict, string, etc
        dataString = json.dumps(data)
        # can only use binary data on sha method so need to convert to bytes
        dataBytes = dataString.encode('utf-8')
        dataHash = SHA256.new(dataBytes) #input must be byte string
        return dataHash

    @staticmethod
    def encode(objectToEncode):
        # unpickable=true lets receiver decode object
        return jsonpickle.encode(objectToEncode, unpicklable=True)

    @staticmethod
    def decode(encodedObject):
        return jsonpickle.decode(encodedObject)
