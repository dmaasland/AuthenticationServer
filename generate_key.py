#!/usr/bin/env python3

from os import path
from os import chmod
from os import makedirs
from shutil import chown
from Crypto.PublicKey import RSA

def main():
    key_dir = path.join(
        path.dirname(path.abspath(__file__)),
        'keys'
    )
    key_file = path.join(
        key_dir,
        'authserver.pem'
    )

    # Create key and directory if it does not exist
    if not path.isdir(key_dir):
        makedirs(
            key_dir
        )

        chown(
            key_dir,
            'nginx',
            'nginx'
        )

        chmod(
            key_dir,
            0o700
        )

    if not path.isfile(key_file):
        key = RSA.generate(
            4096
        )
        
        # Write key to file
        pem = key.export_key(
            'PEM'
        )

        with open(key_file, 'wb') as f:
            f.write(pem)       

        # Set permissions
        chown(
            key_file,
            'nginx',
            'nginx'
        )

        chmod(
            path=key_file,
            mode=0o400
        )

    else:
        # Refuse
        print('Keyfile exists! Delete to continue.')
        exit(1)

if __name__ == '__main__':
    main()