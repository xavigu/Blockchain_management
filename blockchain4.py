from functools import reduce
import hashlib
import json

MINING_REWARD = 10

genesis_block = {
    'previous_hash': '', 
    'index': 0, 
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Javier'
# create a set to the participants of the transactions
participants = {'Javier'}

# Extraer el ultimo valor que tiene el blockchain
# En una lista utilizando -1 accedes al valor que este más a la izquierda de la lista/array y no da error si esta vacio 
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# ----------------------------------------------------
# Add transaction appending to the open_transactions
def add_transaction(recipient, sender=owner, amount=1.0):
    transaction = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        # Add the participants into the set (automatically ignore a value if is duplicated)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False

# ----------------------------------------------------
# Function to verify if a transaction is possible
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    # return true if the sender_balance is greater than the transaction amount otherwise false
    return sender_balance >= transaction['amount']

    
# ----------------------------------------------------
# function to create hashed block
def create_hash_block(block):
    # hash the block and convert to string with json library and encode to utf-8 and hexdigest to have normal characters
    hash_block = hashlib.sha256(json.dumps(block).encode()).hexdigest()
    return hash_block

# ----------------------------------------------------
# function to create a new hash using the transactions, the hash of the last block and a proof number
def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    print(guess_hash)
    # check if the hash start with two zeros at the beginning to return true(valid)
    return guess_hash[0:2] == '00'

# ----------------------------------------------------
# function to get a new proof value
def proof_of_work():
    # get the first list element from the right
    last_block = blockchain[-1]
    last_hash = create_hash_block(last_block)
    while valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof    

# ----------------------------------------------------
# function to calculate the balance amount of a participant
def get_balance(participant):
    # nested list comprehensions to get the transactions where the participant is the sender
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    # amount_sent = 0
    # for tx in tx_sender:
    #     if len(tx) > 0:
    #         amount_sent += tx[0]
    # nested list comprehensions to get the transactions where the participant is the recipient
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant ] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    # amount_received = 0
    # for tx in tx_recipient:
    #     if len(tx) > 0:
    #         amount_received += tx[0]
    return amount_received - amount_sent

# ----------------------------------------------------
#  create a block with the open_transactions and add it to the blockchain
def mine_block():
    last_block = blockchain[-1]
    # el previous_hash será el ultimo block del blockchain pasado a string y separado los valores del dictionary por '-'
    hashed_block = create_hash_block(last_block)
    print(hashed_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    # create a copy of open transactions to dont modified when we append the reward transaction
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': copied_transactions
    }
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
# Comprueba que el primer valor de la segunda blockchain coincide con el valor de la blockchain previa
def verify_chain():
    # usando la funcion enumerate para una lista te da el index por cada elemento(bloque en este caso) de la misma
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        # compara el valor del previous_hash de un block con la creación de un hash_block del bloque anterior
        if block['previous_hash'] != create_hash_block(blockchain[index - 1]):
            return False
    return True    

# ----------------------------------------------------
# Verify all transactions are valid
def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions] )   

# ----------------------------------------------------
# variable to finish the while loop
waiting_for_input = True

# while loop
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('3: Mine a new block')
    print('4: Output the participants')
    print('5: Check transaction validity')
    print('e: Manipulate a blockchain block')
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
    elif user_choice == '4':
        print_participants()
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid!')
        else:
            print('There are invalid transactions')
    elif user_choice == 'e':
        if len(blockchain) >= 1:
            blockchain[0] = {'previous_hash': '', 'index': 0, 'transactions': [{'sender':'Chris', 'recipient':'Tom', 'amount':10.5}]}
    elif user_choice == 'q': 
        waiting_for_input = False
    else:
        print('Input was invalid!!')
    if not verify_chain():
        print_blockchain_blocks()
        print('The blockchain was modified, Invalid!')
        break
    print('Balance of {}:{:6.2f}'.format('Javier', get_balance('Javier')))



