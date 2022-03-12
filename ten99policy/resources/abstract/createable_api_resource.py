from __future__ import absolute_import, division, print_function

from ten99policy.resources.abstract.api_resource import APIResource
from ten99policy import api_requestor, util


class CreateableAPIResource(APIResource):
    @classmethod
    def create(
        cls,
        api_key=None,
        idempotency_key=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key
        )
        url = cls.class_url()
        headers = util.populate_headers(idempotency_key)
        response = requestor.request("post", url, params, headers)

        return response
