blockchain = []

# Extraer el ultimo valor que tiene el blockchain
# En una lista utilizando -1 accedes al valor que este más a la izquierda de la lista/array y no da error si esta vacio 
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(new_transaction=5, last_transaction=[1]):
    """En la funcion se esta añadiendo al blockchain original un array con el ultimo valor 
       del blockchain añadiendo a esa array como ultimo valor la nueva transaction"""
    if last_transaction == None:
        last_transaction = [1]
    blockchain.append([last_transaction, new_transaction])

def get_transaction_value():
    return float(input('Introduce you transaction amount: '))

def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

def print_blockchain_blocks():
    for block in blockchain:
        print('Outputting block')
        print(block)

# Comprueba que el primer valor de la segunda blockchain coincide con el valor de la blockchain previa
def verify_chain():
    # block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    # for block in blockchain:
    #     print('blockchain previous: ', blockchain[block_index - 1])
    #     if block_index == 0:
    #         print('First iteration with block_index 0')
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         print('True')
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1 
    return is_valid    

# ----------------------------------------------------

waiting_for_input = True

# while loop
while waiting_for_input:
    print('Please choose: ')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('e: Manipulate a blockchain block')
    print('q: Finish the transactions')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_amount = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_blocks()
    elif user_choice == 'e':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q': 
        waiting_for_input = False
    else:
        print('Input was invalid!!')
    if not verify_chain():
        print('The blockchain was modified, Invalid!')
        waiting_for_input = False
        



