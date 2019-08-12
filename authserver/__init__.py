from flask import Flask

from authserver.models import AuthenticationServer

app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')
authentication_server = AuthenticationServer(app.config)

import authserver.views
