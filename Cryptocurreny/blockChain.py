import datetime
import hashlib
import json
import requests
from urllib.parse import urlparse

# requests are used to get the response from the flask so that each node have same copy of data
#
# 1. Building Cryptocurrency using BlockChain


class BlockChain:
    def __init__(self):
        self.chain = []  # list containg the blocks
        self.transactions = []  # list for containing transaction which needed to be added in block by miners
        self.create_block(proof_of_work=1, previous_hash='0')  # Genesis block
        self.nodes = set()

    def create_block(self, proof_of_work, previous_hash):
        """
        function to create a block
        :param proof_of_work: for the proof of the work i.e. Nonce
        :param previous_hash: for the link between blocks
        :return the block mined
        """
        # dict for storing the keys of block which are data, block_number, previous_hash, proof, timestamp
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof_of_work,
                 'previous_hash': previous_hash,
                 'data': 'This is block ' + str(len(self.chain) + 1),
                 'transactions': self.transactions}

        # once transactions are added to block then the txn list must become empty
        self.transactions = []
        # to append block in blockchain
        self.chain.append(block)

        # for return data to postman
        return block

    def get_previous_block(self):
        """
        :return the previous block in the chain
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        method to find proof_of_work(POW)
        :param previous_proof: for other miners to verify that the mined block POW is correct
        :return proof of work
        """
        new_proof = 1  # variable for getting the right proof for the problem
        check_proof = False  # for checking that the found proof is correct or not

        while check_proof is False:
            # for making operation non symmetrical ie no two blocks have same proof for every two blocks
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation.startswith('0000'):
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        """
        method that return the SHA256 crypt of the block
        :param block: whose hash is to be find
        :return hash of the block data
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()  # .dumps() convert JSON to string
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """
        method to check whether chain is valid based on previous hash and proof of work
        :param chain: block chain
        :return bool based on the validity of chain
        """
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            current_block = chain[block_index]

            # check for the blocks previous hash
            if current_block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            current_proof = current_block['proof']
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            # hash doesnt starts with 0000 the chain is invalid
            if not hash_operation.startswith('0000'):
                return False

            previous_block = current_block
            block_index += 1

        return True

    def add_transaction(self, sender, receiver, amount):
        """
        method for creating txn between sender and receiver, amount
        :param sender: the sender of the money
        :param receiver: one who is getting the money
        :param amount: value of money transacted
        :return: index of block which will receive these txn
        """
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, node_address):
        """
        method to add node to the network. here we will just change the port number for adding nodes keeping the ip on
        localhost
        :param node_address: the address of the node (127.0.0.1:5001, etc)
        :return: None
        """
        # urlparse--> ParseResult(scheme='https', netloc='127.0.0.1:5000', path='/', params='', query='', fragment='')
        parsed_url = urlparse(node_address)
        # netloc return the address along with port which is to included in the node set
        self.nodes.add(parsed_url.netloc)
        print(self.nodes)

    def replace_chain(self):
        """
        method which will follow consensus protocol and replace the short chain by the longest chain
        in the network again and again. this method is applied to specific node only
        :return: boolean based if the chain is replaced with longest chain in node or node
        """
        network = self.nodes  # network contain all nodes in network
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get('http://' + node + '/get_chain')
            print(response)
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        print(longest_chain)
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
