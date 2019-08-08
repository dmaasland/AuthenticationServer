from os import path
from os import makedirs
from os import chmod

from Crypto.PublicKey import RSA

class AuthenticationServer:
    def __init__(self, config):
        # Initialize variables
        self.key    = None
        self.public = None
        self.key_file = config['PRIVATE_KEY']
        self.network_name = config['NETWORK_NAME']

        # Load keys
        self.check_keys()

    def check_keys(self):
        # Create key if it does not exist
        if not path.isfile(self.key_file):
            self.key = RSA.generate(
                4096
            )

            # Write keys to file
            pem = self.key.export_key(
                'PEM'
            )

            with open(self.key_file, 'wb') as f:
                f.write(pem)       

            # Set permissions
            chmod(
                path=self.key_file,
                mode=0o400
            )

        else:
            # Load existing key from file
            with open(self.key_file, 'rb') as f:
                self.key = RSA.import_key(
                    f.read()
                )

        self.public = self.key.publickey()
