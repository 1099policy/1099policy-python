from __future__ import absolute_import, division, print_function

# Configuration variables

client_id = None
api_base = "http://localhost:5000"
api_key = 't9sk_test_c1fd07b3-edcb-4b76-9eb2-c384a1b8a32b'
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
max_network_retries = 0

# Set to either 'debug' or 'info', controls console logging
log = 'debug'

# API resources
from t99.api_resources import *  # noqa
