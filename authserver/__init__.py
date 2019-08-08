from flask import Flask

from authserver.models import AuthenticationServer

app = Flask(__name__)
app.config.from_object('config')
authentication_server = AuthenticationServer(app.config)

import authserver.views
