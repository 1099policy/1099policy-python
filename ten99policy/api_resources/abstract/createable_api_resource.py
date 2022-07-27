from __future__ import absolute_import, division, print_function

from ten99policy.api_resources.abstract.api_resource import APIResource
from ten99policy import api_requestor, util


class CreateableAPIResource(APIResource):
    @classmethod
    def create(
        cls,
        api_key=None,
        idempotency_key=None,
        ten99policy_version=None,
        ten99policy_environment=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key, api_version=ten99policy_version, environment=ten99policy_environment
        )
        url = cls.class_url()
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request("post", url, params, headers)

        return util.convert_to_ten99policy_object(
            response, api_key, ten99policy_version, ten99policy_environment
        )
