from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet.txt', mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                    print('Keys saved!')
            except (IOError, IndexError):
                print('Saving wallet failed!')        


    def load_keys(self):
        try:
            with open('wallet.txt', mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key           
        except (IOError, IndexError):
            print('Loading wallet failed!')

    def generate_keys(self):
        key = RSA.generate(1024)
        private_key = key.export_key(format='DER')
        public_key = key.publickey().export_key(format='DER')
        return (binascii.hexlify(private_key).decode('ascii'),
                binascii.hexlify(public_key).decode('ascii'))

    "Create string signature"
    def sign_transaction(self, sender, recipient, amount):
        signer = pkcs1_15.new(RSA.import_key(binascii.unhexlify(self.private_key)))
        # payload in a hash form
        hash_payload = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(hash_payload)
        return binascii.hexlify(signature).decode('ascii')


# wallet = Wallet()
# print(wallet.generate_keys())