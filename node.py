from flask import Flask, jsonify
# cors allows the clients running on the same server can access this server
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

# with the name argument you tell flask in which context it runs
app = Flask(__name__)
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
CORS(app)

# decorator to run the function when we pass the endpoint of the argument and the CRUD methods that support (app is like the variable where we instantiate the Flask)
@app.route('/', methods=['GET'])
def get_ui():
    return 'works!'

@app.route('/chain', methods=['GET'])
def get_chain():
    blockchain_snapshot = blockchain.get_blockchain()
    dict_blockchain = [block.__dict__.copy() for block in blockchain_snapshot]
    for dict_block in dict_blockchain:
      dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_blockchain), 200

@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Adding a block successfully',
            'block': dict_block
        }
        return jsonify(response), 201 
    else:
        response = {
            'message': 'Adding a block failed',
            'wallet_set_up': wallet.public_key != None,
        }
        return jsonify(response), 500 


if __name__ == '__main__':
    # run take de IP on which we want to run and the port to listen
    app.run(host='0.0.0.0', port=5000)

  