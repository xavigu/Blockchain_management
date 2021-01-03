genesis_block = {'previous_hash': '', 'index': 0, 'transactions': []}
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
    """
     Arguments:
       :sender: The sender of the coins
       :recipient: The recipient of the coins
       :amount: The amount of coins sent with the transactions
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    open_transactions.append(transaction)
    # Add the participants into the set (automatically ignore a value if is duplicated)
    participants.add(sender)
    participants.add(recipient)

# ----------------------------------------------------
# function to create hashed block
def create_hash_block(block):
    return '-'.join([str(block[key]) for key in block])   

# ----------------------------------------------------
#  create a block with the open_transactions and add it to the blockchain
def mine_block():
    last_block = blockchain[-1]
    # el previous_hash será el ultimo block del blockchain pasado a string y separado los valores del dictionary por '-'
    hashed_block = create_hash_block(last_block)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': open_transactions
    }
    blockchain.append(block)

# ----------------------------------------------------
# Functions to get the inputs that the user write
def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = input('Enter the amount of the transaction: ')
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
# variable to finish the while loop
waiting_for_input = True

# while loop
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('3: Mine a new block')
    print('4: Output the participants')
    print('e: Manipulate a blockchain block')
    print('q: Finish the transactions')
    user_choice = get_user_choice()
    if user_choice == '1':  
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == '2':
        print_blockchain_blocks()
    elif user_choice == '3':
        mine_block()
    elif user_choice == '4':
        print_participants()
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

        



