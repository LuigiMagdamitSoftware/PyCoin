import hashlib as hasher
import datetime as date
import cPickle as pickle

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block(str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash))
        self.nonce = 0

    def hash_block(self, hash_input):
        sha = hasher.sha256()
        sha.update(hash_input)
        return sha.hexdigest()

    def mine_valid_hash(self, difficulty, hash_input):
        hash_requirement = ('0' * difficulty)
        nonce = 0
        if self.hash.startswith(hash_requirement) == False:
            while True:
                hash_check = self.hash_block(str(hash_input) + str(nonce) + str(self.timestamp))
                if hash_check.startswith(hash_requirement):
                    self.hash = hash_check
                    self.nonce = nonce
                    print "Current: " + self.hash
                    print "Last: " + self.previous_hash + '\n'
                    break
                else:
                    nonce = nonce + 1
class Blockchain:
    def __init__(self, coin_name, difficulty, miner_address):
        self.coin_name = coin_name
        self.difficulty = difficulty
        self.miner_address = miner_address
        self.blockchain = [self.create_genesis_block()]
        self.reward = 5
        self.transactions = []
    def create_genesis_block(self):
        return Block(0, date.datetime.now(), [], "0")
    def load_local_ledger(self):
        try:
            print "Local Blockchain file found!"
            self.blockchain = pickle.load(open("Blockchain.pkl", "rb"))
        except Exception as e:
            print str(e)
            print "Could not load blockchain file."
    def calculate_wallet(self, public_address):
        total = 0
        for block in self.blockchain:
            block_total = 0
            for txn in block.data:
                print txn
                if txn["receiver"]==public_address:
                    block_total+=txn["amount"]
            total+=block_total
        print total
    def next_block(self, last_block):
        this_index = last_block.index + 1
        this_timestamp = date.datetime.now()
        this_data = "This is a block" + str(this_index)
        this_hash = last_block.hash
        return Block(this_index, this_timestamp, this_data, this_hash)
    def start_mine(self):
        while True:
            previous_block = self.blockchain[-1]
            block_to_add = self.next_block(previous_block)
            block_to_add.data = self.transactions
            block_to_add.mine_valid_hash(self.difficulty, previous_block.data)

            self.blockchain.append(block_to_add)
            print str(self.reward) + " " + self.coin_name + " has been mined."
            self.transactions = []
            self.create_transaction(self.coin_name+"-network", self.miner_address, self.reward)
            previous_block = block_to_add
            with open('Blockchain.pkl', 'wb') as f:
                pickle.dump(self.blockchain, f, pickle.HIGHEST_PROTOCOL)
    def create_transaction(self, sender, receiver, amount):
        transaction = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "timestamp": str(date.datetime.now())
        }
        print transaction
        self.transactions.append(transaction)

blockchain = Blockchain("Werner Coin", 4, "0")
blockchain.load_local_ledger()
blockchain.calculate_wallet("0")
blockchain.start_mine()

