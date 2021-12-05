from __future__ import absolute_import, division, print_function

from t99 import api_requestor, util
from t99.api_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    def auto_paging_iter(cls, *args, **params):
        return cls.list(*args, **params).auto_paging_iter()

    @classmethod
    def list(
        cls, api_key=None, t99_version=None, t99_account=None, **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key,
            api_base=cls.api_base(),
            api_version=t99_version,
            account=t99_account,
        )
        url = cls.class_url()
        response, api_key = requestor.request("get", url, params)
        t99_object = util.convert_to_t99_object(
            response, api_key, t99_version, t99_account
        )

        # cemre burayi sildi
        # t99_object._retrieve_params = params
        return t99_object
