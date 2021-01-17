from uuid import uuid4
from blockchain import Blockchain
from utils.verification import Verification

class Node:
  # ----------------------------------------------------
    def __init__(self):
        # self.id = str(uuid4())
        self.id = 'Javier'
        self.blockchain = Blockchain(self.id)


    # Functions to get the inputs that the user write
    def get_transaction_value(self):
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Enter the amount of the transaction: '))
        # return a tuple
        return (tx_recipient, tx_amount)

    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input
    # ----------------------------------------------------

    # ----------------------------------------------------
    # Print blocks of the blockchain
    def print_blockchain_blocks(self):
        for block in self.blockchain.get_blockchain():
            print('Outputting block')
            print(block)
        else:
            print('-' * 20)

    # Input main class
    def listen_for_input(self):
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
          user_choice = self.get_user_choice()
          if user_choice == '1':  
              tx_data = self.get_transaction_value()
              recipient, amount = tx_data
              if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                  print('Added transaction!')
              else:
                  print('Transaction failed!')
              print(self.blockchain.get_open_transactions())
          elif user_choice == '2':
              self.print_blockchain_blocks()
          elif user_choice == '3':
              self.blockchain.mine_block()
          elif user_choice == '4':
              if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                  print('All transactions are valid!')
              else:
                  print('There are invalid transactions')
          elif user_choice == 'q': 
              waiting_for_input = False
          else:
              print('Input was invalid!!')
          if not Verification.verify_chain(self.blockchain.get_blockchain()):
              self.print_blockchain_blocks()
              print('The blockchain was modified, Invalid!')
              break
          print('Balance of {}:{:6.2f}'.format(self.id, self.blockchain.get_balance()))

# Run UI Input
node = Node()
node.listen_for_input()