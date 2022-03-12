from __future__ import absolute_import, division, print_function

from ten99policy.resources.abstract.api_resource import APIResource
from ten99policy.six.moves.urllib.parse import quote_plus
from ten99policy import api_requestor, util


class DeletableAPIResource(APIResource):
    @classmethod
    def delete(
        cls,
        sid,
        api_key=None,
        idempotency_key=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key
        )
        url = "%s/%s" % (cls.class_url(), quote_plus(util.utf8(sid)))
        headers = util.populate_headers(idempotency_key)
        response = requestor.request("delete", url, params, headers)

        return response
