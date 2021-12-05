from __future__ import absolute_import, division, print_function

import json
from collections import OrderedDict


class T99ResponseBase(object):
    def __init__(self, code, headers):
        self.code = code
        self.headers = headers

    @property
    def idempotency_key(self):
        try:
            return self.headers["idempotency-key"]
        except KeyError:
            return None

    @property
    def request_id(self):
        try:
            return self.headers["request-id"]
        except KeyError:
            return None


class T99Response(T99ResponseBase):
    def __init__(self, body, code, headers):
        T99ResponseBase.__init__(self, code, headers)
        self.body = body
        self.data = json.loads(body, object_pairs_hook=OrderedDict)


class T99StreamResponse(T99ResponseBase):
    def __init__(self, io, code, headers):
        T99ResponseBase.__init__(self, code, headers)
        self.io = io
