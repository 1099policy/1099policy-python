from __future__ import absolute_import, division, print_function

# Configuration variables

client_id = None
api_base = "https://api.1099policy.com"
# No default key. Every release up to 1.1.12 shipped a real sandbox key
# here, so anyone who installed the package and never set their own was
# authenticating as that organization. Set `ten99policy.api_key` yourself;
# a request made without one raises AuthenticationError with the hint.
api_key = None
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None
max_network_retries = 0
environment = 'sandbox'

# Set to either 'debug' or 'info', controls console logging
log = 'debug'

# API resources
from ten99policy.api_resources import *  # noqa
