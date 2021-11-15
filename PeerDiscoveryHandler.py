import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils

"""
@function: submodule of p2p comm. frequently comm with network to see if new nodes to discover
"""
class PeerDiscoveryHandler:

    def __init__(self, node):
        self.socketCommunication = node

    # start status and discovery methods
    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        discoveryThread = threading.Thread(target=self.discovery, args=())
        discoveryThread.start()

    def status(self):
        while True:
            print('current connections:')
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ":" + str(peer.port))
            time.sleep(10)

    # sending broadcast message into the network so other nodes can hear which connections this specific node has
    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    # one node connect to other node
    def handshake(self, connect_node):
        handshakeMessage = self.handshakeMessage()
        self.socketCommunication.send(connect_node, handshakeMessage)

    # use helper class message to construct specific message with purpose of peer discoery
    # send message containing the data of the connected nodes (or known nodes) to the other nodes that want to connect to us
    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    """
    1) check if we are already a peer with the message sender (we are receiver here), if not, add it to our peer list
    2) check in peers peer list if there are new peers we should also connect to
    """
    def handleMessage(self, message):
        peersSocketConnector = message.senderConnector
        peersPeerList = message.data
        newPeer = True
        # check if peers already exist in our list. if so don't add
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer:
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector): # make sure not ourselves
                self.socketCommunication.connect_with_node(peersPeer.ip, peersPeer.port) # connect with new peer


