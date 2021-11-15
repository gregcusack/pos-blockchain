from p2pnetwork.node import Node
from PeerDiscoveryHandler import PeerDiscoveryHandler
from SocketConnector import SocketConnector
from BlockchainUtils import BlockchainUtils
import json


class SocketCommunication(Node):

    def __init__(self, ip, port):
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = [] # TODO: this probably could be better data structure
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)

    """
    @info: allows the new node to join the network and connect to all other nodes. here we assume that there is one
    node that is always online. we call that the "First Node" at it runs on port 10001. i'm sure this is not the 
    best way to do it though. Should look at options to see what some other methods are for creating a node and joining 
    the network
    """
    def connectToFirstNode(self):
        if self.socketConnector.port != 10001: # as long as we are not running on port 10001, we conenct to it
            self.connect_with_node('localhost', 10001)

    def startSocketCommunication(self, node):
        self.node = node
        self.start()  # calls start socket comm using ip and port
        self.peerDiscoveryHandler.start()
        self.connectToFirstNode()

    def inbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)  # send msg back when node connects to you

    def outbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)  # send msg to node you're connecting to

    # receiving message inbound. message here will be from handshake() method
    # need to decode message we're receiving and figure out what submodule needs to handle the incoming message
    # figure it out based on messageType
    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':  # need to sent newly received tx to other nodes in network
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == 'BLOCK':
            block = message.data
            self.node.handleBlock(block)
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockchainRequest(connected_node)
        elif message.messageType == 'BLOCKCHAIN':
            blockchain = message.data
            self.node.handleBlockchain(blockchain)


    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)  # broadcast message

