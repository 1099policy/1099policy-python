from __future__ import absolute_import, division, print_function

import os

# Configuration variables

api_base = "http://localhost:5000"
api_key = 't9sk_test_f2d75006-2825-4ade-8ff8-71e81809eb2a'
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
max_network_retries = 0

# Set to either 'debug' or 'info', controls console logging
log = 'debug'

# API resources
from t99.api_resources import *  # noqa
