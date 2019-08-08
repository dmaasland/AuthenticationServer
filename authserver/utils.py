import xml.etree.ElementTree as ET

from Crypto import Random
from Crypto.Hash import SHA1
from Crypto.Signature import pkcs1_15

from base64 import b64encode
from base64 import b64decode

def create_signature(authentication_server, client_random_b64):
    # Generate 64 random bytes
    server_random = Random.get_random_bytes(
        64
    )

    client_random = b64decode(
        client_random_b64
    )

    # Create SHA1 digest
    digest = SHA1.new()
    
    # Client random
    digest.update(
        client_random
    )

    # Add server_random
    digest.update(
        server_random
    )
    
    # Create signature
    pkcs = pkcs1_15.new(
        authentication_server.key
    )
    
    signature = pkcs.sign(
        digest
    )

    return server_random, signature

def build_xml(authentication_server, server_random, signature):
    # Base64 encode server_random and the signature
    server_random_b64 = b64encode(
        server_random
    ).decode(
        'utf-8'
    )

    signature_b64 = b64encode(
        signature
    ).decode(
        'utf-8'
    )

    # Construct the XML
    root = ET.Element('ESET')
    doc = ET.SubElement(root, 'SERVER_AUTH')

    ET.SubElement(
        doc,
        'NODE',
        NAME='Status',
        VALUE='OK',
        TYPE='STRING'
    )

    ET.SubElement(
        doc,
        'NODE',
        NAME='Zone',
        VALUE=authentication_server.network_name,
        TYPE='STRING'
    )

    ET.SubElement(
        doc,
        'NODE',
        NAME='Version',
        VALUE='1',
        TYPE='DWORD'
    )
    
    ET.SubElement(
        doc,
        'NODE',
        NAME='Server_Random',
        VALUE=server_random_b64,
        TYPE='BINARY'
    )

    ET.SubElement(
        doc,
        'NODE',
        NAME='Sign',
        VALUE=signature_b64,
        TYPE='BINARY'
    )

    xml = ET.tostring(
        root,
        encoding="utf8",
        method="xml"
    ).decode(
        'utf-8'
    )
    
    # Replace single quotes in XML declaration
    xml = xml.replace(
        '\'',
        '"'
    )

    return xml