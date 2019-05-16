from flask import Flask, jsonify
import blockChain

app = Flask(__name__)

# create blockchain
blockchain = blockChain.BlockChain()


@app.route('/mine_block', methods=['GET'])
def mine_block():
    """
    Mining the block
    """
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congrats you mined a block!!!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'data': block['data']}
    return jsonify(response), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    getting whole chain
    :return: whole chain
    """
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


@app.route('/is_valid', methods = ['GET'])
def is_valid():
    """
    checking is block chain valid
    :return: json object containing chain
    """
    is_valid_chain = blockchain.is_chain_valid(blockchain.chain)

    if is_valid_chain:
        response = {'message': 'Congrats! Chain is valid'}
    else:
        response = {'message': 'Alas! Invalid Chain'}

    return jsonify(response)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = '5000')
