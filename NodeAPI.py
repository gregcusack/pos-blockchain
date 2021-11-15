from flask_classful import FlaskView, route
from flask import Flask, jsonify, request
from BlockchainUtils import BlockchainUtils
node = None

"""
@info user api. users interact with the node rest api to send transactions
"""
class NodeAPI(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)  # create flask app

    def start(self, apiPort):
        NodeAPI.register(self.app, route_base='/')
        self.app.run(host='localhost', port=apiPort)

    def injectNode(self, injectedNode):
        global node # have to do this due to some architectural issues with FlaskView
        node = injectedNode

    @route('/info', methods=['GET'])
    def info(self):
        return 'this is a comm interface to a nodes blockchain\n', 200

    @route('/blockchain', methods=['GET'])
    def blockchain(self):
        return node.blockchain.toJson(), 200

    @route('/transactionPool', methods=['GET'])
    def transactionPool(self):
        transactions = {}
        # ctr just counts iterations
        for ctr, transaction in enumerate(node.transactionPool.transactions):
            transactions[ctr] = transaction.toJson()
        return jsonify(transactions), 200

    @route('/transaction', methods=['POST'])
    def transaction(self):
        values = request.get_json()  # TODO: expects json formatted data. must error check
        if not 'transaction' in values:
            return 'Missing transaction value', 400
        transaction = BlockchainUtils.decode(values['transaction'])
        node.handleTransaction(transaction)
        response = {'message': 'received transaction'}
        return jsonify(response), 201


