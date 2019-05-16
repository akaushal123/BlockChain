from flask import Flask, jsonify, request
import blockChain
from uuid import uuid4


# it generates a random and unique address of the node
# request are used for connect nodes and getting data from them using getjson method

# creating webApp
app = Flask(__name__)

# it is added as miner also get some coins and the txn is also to be completed
# uuid4() generates unique address for the nodes, it has - between then, which need to be replaced
# creating an address for the node on port 5000
node_address = str(uuid4()).replace("-", "")

# create blockchain
blockchain = blockChain.BlockChain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    """
    For mining the block
    :return: json object along with response code
    """
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    # consider as miner node, so receiver is self
    blockchain.add_transaction(sender=node_address, receiver='Pranav', amount=10)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats you mined a block!!!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'data': block['data'],
                'transactions': block['transactions']
                }

    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    getting the block chain
    :return: chain and its length as json
    """
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}

    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    """
    checking validity of chain
    :return: json object displaying the message about chain validity
    """
    is_valid_chain = blockchain.is_chain_valid(blockchain.chain)

    if is_valid_chain:
        response = {'message': 'Congrats! Chain is valid'}
    else:
        response = {'message': 'Alas! Invalid Chain'}

    return jsonify(response)


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    """
    add new txn to block
    :return: json object stating the message about txn addition in block
    """
    json = request.get_json()  # json will have the txn details
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in json for key in transaction_keys):
        return 'Some elements of transaction missing', 400

    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = {'message': 'This transaction will be added in Block ' + str(index)}

    return jsonify(response), 201


@app.route('/connect_node', methods=['POST'])
def connect_node():
    """
    connecting new nodes to the network
    :return: json object and list of nodes in block chain
    """
    json = request.get_json()  # json will have the list of all nodes in network
    nodes = json.get('nodes')  # key of the value of node address

    if nodes is None:
        return 'No Node', 401

    for node in nodes:
        blockchain.add_node(node)

    response = {'message': 'All the nodes are now connected. The block chain contains following nodes',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201


@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    """
    replacing chain by longest chain if needed longest
    :return: message and chain as json object
    """
    is_chain_replaced = blockchain.replace_chain()

    if is_chain_replaced:
        response = {'message': 'Nodes had different chain. Chain in node is replaced by longest one',
                    'new_chain': blockchain.chain
                    }
    else:
        response = {'message': 'All good. The chain is largest one',
                    'actual_chain': blockchain.chain
                    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
