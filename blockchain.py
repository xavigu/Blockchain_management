from functools import reduce
from collections import OrderedDict
import hashlib
import json

from utils.hash_util import create_hash_block
from utils.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet

MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        self.__blockchain = [genesis_block]
        self.__open_transactions = []
        # execute inmediatelly the load_data when we run the script
        self.load_data()
        self.hosting_node = hosting_node_id
        # set where we storage the nodes by participant
        self.__peer_nodes = set()

    def get_blockchain(self):
        return self.__blockchain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    # load transactions data of a file
    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                # blockchain logic 
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_transactions = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_transactions, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block) 
                self.__blockchain = updated_blockchain
                # open_transactions logic
                open_transactions = json.loads(file_content[1][:-1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) 
                    updated_transactions.append(updated_transaction) 
                self.__open_transactions = updated_transactions
                # peer_nodes logic
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
           print('Handled exception...')
        finally:
            print('Cleanup!')


    # save transactions data in a file
    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain.txt', mode='w') as f:
                # save the block object like a dictionary
                saveable_chain = [block.__dict__ for block in 
                [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions] , block_el.proof, block_el.timestamp) 
                for block_el in self.__blockchain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_transactions = [tx.__dict__ for tx in self.__open_transactions]
                f.write(json.dumps(saveable_transactions))
                # save the connected nodes
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))                
        except IOError:
            print('Saving failed')

    # ----------------------------------------------------
    # function to get a new proof value
    def proof_of_work(self):
        # get the first list element from the right
        last_block = self.__blockchain[-1]
        last_hash = create_hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof    

    # ----------------------------------------------------
    # function to calculate the balance amount of a participant
    def get_balance(self):
        if self.hosting_node == None:
            return None        
        participant = self.hosting_node
        # nested list comprehensions to get the transactions where the participant is the sender
        tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__blockchain]
        open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # amount_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         amount_sent += tx[0]
        # nested list comprehensions to get the transactions where the participant is the recipient
        tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant ] for block in self.__blockchain]
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # amount_received = 0
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #         amount_received += tx[0]
        # Return the total balance
        return amount_received - amount_sent

    # Extraer el ultimo valor que tiene el blockchain
    # En una lista utilizando -1 accedes al valor que este más a la izquierda de la lista/array y no da error si esta vacio 
    def get_last_blockchain_value(self):
        if len(self.__blockchain) < 1:
            return None
        return self.__blockchain[-1]

    # ----------------------------------------------------
    # Add transaction appending to the open_transactions
    def add_transaction(self, recipient, sender, signature, amount=1.0):
        if self.hosting_node == None:
            return False
        # Create transaction class object
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    # ----------------------------------------------------
    #  create a block with the open_transactions and add it to the blockchain
    def mine_block(self):
        if self.hosting_node == None:
            return None
        last_block = self.__blockchain[-1]
        # el previous_hash será el ultimo block del blockchain pasado a string y separado los valores del dictionary por '-'
        hashed_block = create_hash_block(last_block)
        # give a new proof value to the current transaction
        proof = self.proof_of_work()
        print(hashed_block)
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        # create a copy of open transactions to dont modified when we append the reward transaction
        copied_transactions = self.__open_transactions[:]
        # Verify all transactions of the block are signed correctly
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__blockchain), hashed_block, copied_transactions, proof)
        self.__blockchain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block

    def add_peer_node(self, node):
        """Adds a new node to the peer node set.

        Arguments:
            :node: The node URL which should be added.
        """    
        self.__peer_nodes(node)   
        self.save_data()

    def remove_peer_node(self, node):
        self.__peer_nodes.discard(node)   
        self.save_data()

