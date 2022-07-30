from __future__ import absolute_import, division, print_function

from ten99policy import api_requestor, util
from ten99policy.api_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(
        cls, api_key=None, ten99policy_version=None, ten99policy_environment=None, **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key,
            api_base=cls.api_base(),
            api_version=ten99policy_version,
            environment=ten99policy_environment,
        )
        url = cls.class_url()
        response, api_key = requestor.request("get", url, params)
        ten99policy_object = util.convert_to_ten99policy_object(
            response, api_key, ten99policy_version, ten99policy_environment
        )

        # CFK: take a look at here
        # ten99policy_object._retrieve_params = params
        return ten99policy_object
