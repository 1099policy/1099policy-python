from __future__ import absolute_import, division, print_function

from ten99policy import api_requestor, util
from ten99policy.api_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(
        cls, api_key=None, **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key,
            api_base=cls.api_base(),
        )
        url = cls.class_url()
        response = requestor.request("get", url, params)
        
        # cemre burayi sildi
        # ten99policy_object._retrieve_params = params
        return response
