from __future__ import absolute_import, division, print_function

import json
from collections import OrderedDict


class Ten99PolicyResponseBase(object):
    def __init__(self, code, headers):
        self.code = code
        self.headers = headers

    @property
    def idempotency_key(self):
        try:
            return self.headers["Ten99Policy-Idempotent-Key"]
        except KeyError:
            return None

    @property
    def request_id(self):
        try:
            return self.headers["request-id"]
        except KeyError:
            return None


class Ten99PolicyResponse(Ten99PolicyResponseBase):
    def __init__(self, body, code, headers):
        Ten99PolicyResponseBase.__init__(self, code, headers)
        self.body = body
        self.data = json.loads(body, object_pairs_hook=OrderedDict)


class Ten99PolicyStreamResponse(Ten99PolicyResponseBase):
    def __init__(self, io, code, headers):
        Ten99PolicyResponseBase.__init__(self, code, headers)
        self.io = io
