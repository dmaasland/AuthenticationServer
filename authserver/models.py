from os import path
from os import makedirs
from os import chmod

from Crypto.PublicKey import RSA

class AuthenticationServer:
    def __init__(self, config):
        # Initialize variables
        self.key    = None
        self.public = None
        self.network_name = config['NETWORK_NAME']
        self.key_file = path.join(
            path.dirname(path.abspath(__file__)),
            '../'
            'keys',
            'authserver.pem'
        )

        # Load keys
        self.load_key()

    def load_key(self):
        with open(self.key_file, 'rb') as f:
            self.key = RSA.import_key(
                f.read()
            )

        self.public = self.key.publickey()
