from flask import request
from flask import Response
from base64 import b64encode

from authserver import app
from authserver import authentication_server
from authserver.utils import create_signature
from authserver.utils import build_xml

@app.route('/')
def send_response():
    # Check if it's a client request
    if request.args.get('Client_Random'):
        client_random_b64 = request.args.get('Client_Random')

        # Fix custom url safe base64
        replace_chars = {
            '-':'+',
            '_':'/',
            ',':'='
        }    

        for find, replace in replace_chars.items():
            client_random_b64 = client_random_b64.replace(
                find,
                replace
            )

        # Get signature and server random bytes    
        signature, server_random = create_signature(authentication_server, client_random_b64)

        # Build response XML file
        response = build_xml(authentication_server, signature, server_random)

        # Return XML
        return Response(response, mimetype='text/xml')
    else:
        # Get current public key
        public_encoded = b64encode(
            authentication_server.public.export_key(
                'DER'
            )
        )
        
        # Show current public key
        return Response(public_encoded, mimetype='text/plain')
