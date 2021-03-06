from flask import Flask, jsonify, request, send_from_directory
# cors allows the clients running on the same server can access this server
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain

# with the name argument you tell flask in which context it runs
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def get_main_ui():
    return send_from_directory('ui', 'node.html')

@app.route('/network', methods=['GET'])
def get_network_ui():
    return send_from_directory('ui', 'network.html')

@app.route('/wallet', methods=['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
          'message': 'Saving the keys failed'
        }
        return jsonify(response), 500      

@app.route('/wallet', methods=['GET'])
def load_keys():
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key, port)
        response = {
            'public_key': wallet.public_key,
            'private_key': wallet.private_key,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
          'message': 'Loading the keys failed'
        }
        return jsonify(response), 500           

@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Fetched balanced successfully',
            'funds': balance
        }
        return jsonify(response), 201
    else:
      response = {
        'message': 'Loading balance failed',
        'wallet_set_up': wallet.public_key != None
      }
      return jsonify(response), 500         


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = {
          'message': 'No wallet set up'
        }
        return jsonify(response), 400      
    # get data passing in the request
    values = request.get_json()
    if not values:
        response = {
          'message': 'Not data found'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    # check in a list like an object if all fields in required_fields if a field is part of the incoming values
    if not all(field in values for field in required_fields):
        response = {
          'message': 'Required data is missing'
        }
        return jsonify(response), 400
    # add transaction logic
    recipient = values['recipient']
    amount = values['amount']
    print(recipient, amount)
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    print('SUCCESS: ', success)
    if success:
        response = {
          'message': 'Successfully added transaction',
          'transaction': {
            'sender': wallet.public_key,
            'recipient': recipient,
            'amount': amount,
            'signature': signature
          },
          'funds': blockchain.get_balance()
        }
        return jsonify(response), 201        
    else:
        response = {
          'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500

@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    open_transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in open_transactions]
    return jsonify(dict_transactions), 200 

@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    required_fields = ['sender', 'recipient', 'amount', 'signature']
    if not values:
        response = {
          'message': 'No data found'
        }
        return jsonify(response), 400
    if not all(key in values for key in required_fields):
        response = {
          'message': 'Some data is missing'
        }
        return jsonify(response), 400
    success = blockchain.add_transaction(values['recipient'], values['sender'], values['signature'], values['amount'], is_receiving=True)
    if success:
        response = {
          'message': 'Successfully added transaction',
          'transaction': {
            'sender': values['sender'],
            'recipient': values['recipient'],
            'amount': values['amount'],
            'signature': values['signature']
          }
        }
        return jsonify(response), 201        
    else:
        response = {
          'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500

@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {
          'message': 'No data found'
        }
        return jsonify(response), 400  
    if 'block' not in values:
        response = {
          'message': 'Some data is missing'
        }
        return jsonify(response), 400              
    block = values['block']
    # check if the block its the same than the latest in the blockchain
    if block['index'] == blockchain.get_blockchain()[-1].index + 1:
        if blockchain.add_block(block):
            response = {
                'message': 'Block added'
              }
            return jsonify(response), 201
        else:
            response = {
                'message': 'Block seems invalid.'
              }
            return jsonify(response), 409                        
    elif block['index'] > blockchain.get_blockchain()[-1].index:
      response = {
          'message': 'Blockchain seems to differ from local blockchain'
        }
      blockchain.resolve_conflicts = True  
      return jsonify(response), 200
    else:
      response = {
          'message': 'Blockchain seems to be shorter, block not added'
        }
      return jsonify(response), 409

@app.route('/chain', methods=['GET'])
def get_chain():
    blockchain_snapshot = blockchain.get_blockchain()
    dict_blockchain = [block.__dict__.copy() for block in blockchain_snapshot]
    for dict_block in dict_blockchain:
      dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_blockchain), 200

@app.route('/mine', methods=['POST'])
def mine():
    if blockchain.resolve_conflicts:
        response = {
            'message': 'Resolve conflicts first, block not added',          
        }
        return jsonify(response), 409
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
        response = {
            'message': 'Adding a block successfully',
            'block': dict_block,
            'funds': blockchain.get_balance()
        }
        return jsonify(response), 201 
    else:
        response = {
            'message': 'Adding a block failed',
            'wallet_set_up': wallet.public_key != None,
        }
        return jsonify(response), 500 

@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {
          'message': 'Chain was replaced!'
        }
    else:
        response = {
          'message': 'Local chain kept'
        }
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
      'all_nodes': nodes
    }
    return jsonify(response), 200

@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
          'message': 'No data attached'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
          'message': 'No node data found'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
      'message': 'Node added successfully',
      'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201

# when you use delete method you need call replacing the <node_url> with the peer_node you want delete
@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == '' or node_url == None:
        response = {
          'message': 'No Node found'
        }
        return jsonify(response), 400          
    blockchain.remove_peer_node(node_url)
    response = {
      'message': 'Node removed successfully',
      'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


if __name__ == '__main__':
    # library to pass arguments when you run the server
    from argparse import ArgumentParser
    parser = ArgumentParser()
    # add the arguments that you can pass when you run the server and add default value
    parser.add_argument('-p', '--port', type=int, default=5000)
    # catch the args in a variable
    args = parser.parse_args()
    # get the port value in the args if you dont pass any value it gets 5000 by default
    port = args.port
    # the variables is available globally in the file because this part runs first
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)

  