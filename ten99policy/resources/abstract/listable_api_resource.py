from __future__ import absolute_import, division, print_function

from ten99policy import api_requestor, util
from ten99policy.resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def list(
        cls,
        api_key=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key,
        )
        url = cls.class_url()
        response = requestor.request("get", url, params)
        
        return response
