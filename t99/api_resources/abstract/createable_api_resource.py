from __future__ import absolute_import, division, print_function

from t99.api_resources.abstract.api_resource import APIResource
from t99 import api_requestor, util


class CreateableAPIResource(APIResource):
    @classmethod
    def create(
        cls,
        api_key=None,
        idempotency_key=None,
        t99_version=None,
        t99_account=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key, api_version=t99_version, account=t99_account
        )
        url = cls.class_url()
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request("post", url, params, headers)

        return util.convert_to_t99_object(
            response, api_key, t99_version, t99_account
        )
