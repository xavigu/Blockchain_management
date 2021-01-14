from functools import reduce
from collections import OrderedDict
import hashlib
import json

from hash_util import create_hash_block
from block import Block
from transaction import Transaction
from verification import Verification

MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = 'Javier'

# load transactions data of a file
def load_data():
    global blockchain
    global open_transactions 
    try:
        with open('blockchain.txt', mode='r') as f:
            file_content = f.readlines()
            # blockchain logic 
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_transactions = [Transaction(
                    tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                updated_block = Block(
                    block['index'], block['previous_hash'], converted_transactions, block['proof'], block['timestamp'])
                updated_blockchain.append(updated_block) 
            blockchain = updated_blockchain
            # open_transactions logic
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx['sender'], tx['recipient'], tx['amount']) 
                updated_transactions.append(updated_transaction) 
            open_transactions = updated_transactions
    except (IOError, IndexError):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        blockchain = [genesis_block]
        # Unhandled transactions
        open_transactions = []
    finally:
        print('Cleanup!')

# execute inmediatelly the load_data when we run the script
load_data()

# save transactions data in a file
def save_data():
    """Save blockchain + open transactions snapshot to a file."""
    try:
        with open('blockchain.txt', mode='w') as f:
            # save the block object like a dictionary
            saveable_chain = [block.__dict__ for block in 
             [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions] , block_el.proof, block_el.timestamp) 
             for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_transactions = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_transactions)) 
    except IOError:
        print('Saving failed')

# ----------------------------------------------------
# function to get a new proof value
def proof_of_work():
    # get the first list element from the right
    last_block = blockchain[-1]
    last_hash = create_hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof    

# ----------------------------------------------------
# function to calculate the balance amount of a participant
def get_balance(participant):
    # nested list comprehensions to get the transactions where the participant is the sender
    tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    # nested list comprehensions to get the transactions where the participant is the recipient
    tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant ] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_received += tx[0]
    # Return the total balance
    return amount_received - amount_sent

# Extraer el ultimo valor que tiene el blockchain
# En una lista utilizando -1 accedes al valor que este más a la izquierda de la lista/array y no da error si esta vacio 
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# ----------------------------------------------------
# Add transaction appending to the open_transactions
def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False

# ----------------------------------------------------
#  create a block with the open_transactions and add it to the blockchain
def mine_block():
    last_block = blockchain[-1]
    # el previous_hash será el ultimo block del blockchain pasado a string y separado los valores del dictionary por '-'
    hashed_block = create_hash_block(last_block)
    # give a new proof value to the current transaction
    proof = proof_of_work()
    print(hashed_block)
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    # create a copy of open transactions to dont modified when we append the reward transaction
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True

# ----------------------------------------------------
# Functions to get the inputs that the user write
def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Enter the amount of the transaction: '))
    # return a tuple
    return (tx_recipient, tx_amount)

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input
# ----------------------------------------------------

# ----------------------------------------------------
# Hacer un print de todos los bloques del blockchain
def print_blockchain_blocks():
    for block in blockchain:
        print('Outputting block')
        print(block)
    else:
        print('-' * 20)

def print_participants():
    print('Participants list: ', participants)

# ----------------------------------------------------
# variable to finish the while loop
waiting_for_input = True

# while loop
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('3: Mine a new block')
    print('4: Check transaction validity')
    print('q: Finish the transactions')
    user_choice = get_user_choice()
    if user_choice == '1':  
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain_blocks()
    elif user_choice == '3':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '4':
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print('All transactions are valid!')
        else:
            print('There are invalid transactions')
    elif user_choice == 'q': 
        waiting_for_input = False
    else:
        print('Input was invalid!!')
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_blocks()
        print('The blockchain was modified, Invalid!')
        break
    print('Balance of {}:{:6.2f}'.format('Javier', get_balance('Javier')))



