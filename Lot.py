from BlockchainUtils import BlockchainUtils

class Lot:

    """
    @info: iteration. higher stake, more iterations you can create where each iteration creates a Lot.
    has something to do with PoS. aka more iterations more likely you're selected as forger. not 100% sure yet
    """
    def __init__(self, publicKey, iteration, lastBlockHash):
        self.publicKey = str(publicKey)
        self.iteration = iteration
        self.lastBlockHash = lastBlockHash

    # used to create hash of lots
    def lotHash(self):
        hashData = self.publicKey + self.lastBlockHash
        for _ in range(self.iteration):
            hashData = BlockchainUtils.hash_(hashData).hexdigest()
        return hashData # this is our lot
