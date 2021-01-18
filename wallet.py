from Crypto.PublicKey import RSA
import binascii


class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    def generate_keys(self):
        key = RSA.generate(1024)
        private_key = key.export_key(format='DER')
        public_key = key.publickey().export_key(format='DER')
        return (binascii.hexlify(private_key).decode('ascii'),
                binascii.hexlify(public_key).decode('ascii'))

# wallet = Wallet()
# print(wallet.generate_keys())