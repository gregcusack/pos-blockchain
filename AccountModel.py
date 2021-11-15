
class AccountModel:

    def __init__(self):
        self.accounts = [] #all accounts
        self.balances = {} # key and balances

    def addAcount(self, publicKeyString):
        if not publicKeyString in self.accounts: # this should be a map or set
            self.accounts.append(publicKeyString)
            self.balances[publicKeyString] = 0

    # TODO not sure we should add an account on getBalance if it doesn't exist
    def getBalance(self, publicKeyString):
        if publicKeyString not in self.accounts:
            self.addAcount(publicKeyString)
        return self.balances[publicKeyString]

    # TODO: should also check for under/overflows!
    # don't add account if doesn't exist!
    # use this method for subtracting balance too. i do not like. should be incr and decr balance methods
    def updateBalance(self, publicKeyString, amount):
        if publicKeyString not in self.accounts:
            self.addAcount(publicKeyString)
        self.balances[publicKeyString] += amount
