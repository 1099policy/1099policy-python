from __future__ import absolute_import, division, print_function

# Configuration variables

api_base = "http://localhost:5000"
api_key = 't9sk_test_1e9712b1-507d-40d9-9c2a-1ff7c2c7f840'
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
max_network_retries = 0

# Set to either 'debug' or 'info', controls console logging
log = 'debug'

# API resources
from t99.api_resources import *  # noqa
