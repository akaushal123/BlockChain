import datetime
import hashlib
import json


# 1. Building Block chain

class BlockChain:

    def __init__(self):
        self.chain = []  # list containg the blocks
        self.create_block(proof_of_work=1, previous_hash='0')  # Genesis block

    def create_block(self, proof_of_work, previous_hash):
        """
        function to create a block
        @:param proof_of_work for the proof of the work i.e. Nonce
       @:param previous_hash for the link between blocks
        """
        # dict for storing the keys of block which are data, block_number, previous_hash, proof, timestamp
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof_of_work,
                 'previous_hash': previous_hash,
                 'data': 'This is block ' + str(len(self.chain) + 1)}

        # to append block in blockchain
        self.chain.append(block)

        # for return data to postman
        return block

    def get_previous_block(self):
        """
        for getting the previous block in the chain
        """
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        method to find proof_of_work(POW)
        @:param previous_proof for other miners to verify that the mined block POW is correct
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
        @:param block whose hash is to be find
        """
        encoded_block = json.dumps(block, sort_keys=True).encode()  # .dumps() convert JSON to string
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        """
        method to check whether chain is valid based on previous hash and proof of work
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
