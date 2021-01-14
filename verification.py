from hash_util import hash_string_256, create_hash_block

class Verification:
    # ----------------------------------------------------
    # function to create a new hash using the transactions, the hash of the last block and a proof number
    def valid_proof(self, transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        # check if the hash start with two zeros at the beginning to return true(valid)
        return guess_hash[0:2] == '00'

    # ----------------------------------------------------
    # Function to verify if a transaction is possible
    def verify_transaction(self, transaction, get_balance):
        sender_balance = get_balance(transaction.sender)
        # return true if the sender_balance is greater than the transaction amount otherwise false
        return sender_balance >= transaction.amount

    # ----------------------------------------------------
    # Comprueba que el primer valor de la segunda blockchain coincide con el valor de la blockchain previa
    def verify_chain(self, blockchain):
        # usando la funcion enumerate para una lista te da el index por cada elemento(bloque en este caso) de la misma
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            # compara el valor del previous_hash de un block con la creación de un hash_block del bloque anterior
            if block.previous_hash != create_hash_block(blockchain[index - 1]):
                return False
            # comprobar que es un valid proof quitando antes del bloque el ultimo valor que corresponde a las reward transaction    
            if not self.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid!')
                return False
        return True    

    # ----------------------------------------------------
    # Verify all transactions are valid
    def verify_transactions(self, open_transactions, get_balance):
        return all([self.verify_transaction(tx, get_balance) for tx in open_transactions] )   