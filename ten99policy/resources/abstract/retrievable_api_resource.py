from __future__ import absolute_import, division, print_function

from ten99policy.resources.abstract.api_resource import APIResource
from ten99policy import api_requestor, util


class RetrievableAPIResource(APIResource):
    @classmethod
    def retrieve(
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
