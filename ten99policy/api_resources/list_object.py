from __future__ import absolute_import, division, print_function

from ten99policy import api_requestor, six, util
from ten99policy.ten99policy_object import Ten99PolicyObject

from ten99policy.six.moves.urllib.parse import quote_plus


class ListObject(Ten99PolicyObject):
    OBJECT_NAME = "list"

    def list(
        self, api_key=None, ten99policy_version=None, ten99policy_environment=None, **params
    ):
        ten99policy_object = self._request(
            "get",
            self.get("url"),
            api_key=api_key,
            ten99policy_version=ten99policy_version,
            ten99policy_environment=ten99policy_environment,
            **params
        )
        ten99policy_object._retrieve_params = params
        return ten99policy_object

    def create(
        self,
        api_key=None,
        idempotency_key=None,
        ten99policy_version=None,
        ten99policy_environment=None,
        **params
    ):
        return self._request(
            "post",
            self.get("url"),
            api_key=api_key,
            idempotency_key=idempotency_key,
            ten99policy_version=ten99policy_version,
            ten99policy_environment=ten99policy_environment,
            **params
        )

    def retrieve(
        self,
        id,
        api_key=None,
        ten99policy_version=None,
        ten99policy_environment=None,
        **params
    ):
        url = "%s/%s" % (self.get("url"), quote_plus(util.utf8(id)))
        return self._request(
            "get",
            url,
            api_key=api_key,
            ten99policy_version=ten99policy_version,
            ten99policy_environment=ten99policy_environment,
            **params
        )

    def _request(
        self,
        method_,
        url_,
        api_key=None,
        idempotency_key=None,
        ten99policy_version=None,
        ten99policy_environment=None,
        **params
    ):
        api_key = api_key or self.api_key
        ten99policy_version = ten99policy_version or self.ten99policy_version
        ten99policy_environment = ten99policy_environment or self.ten99policy_environment

        requestor = api_requestor.APIRequestor(
            api_key, api_version=ten99policy_version, environment=ten99policy_environment
        )
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request(method_, url_, params, headers)
        ten99policy_object = util.convert_to_ten99policy_object(
            response, api_key, ten99policy_version, ten99policy_environment
        )
        return ten99policy_object

    def __getitem__(self, k):
        if isinstance(k, six.string_types):
            return super(ListObject, self).__getitem__(k)
        else:
            raise KeyError(
                "You tried to access the %s index, but ListObject types only "
                "support string keys. (HINT: List calls return an object with "
                "a 'data' (which is the data array). You likely want to call "
                ".data[%s])" % (repr(k), repr(k))
            )

    def __iter__(self):
        return getattr(self, "data", []).__iter__()

    def __len__(self):
        return getattr(self, "data", []).__len__()

    def __reversed__(self):
        return getattr(self, "data", []).__reversed__()

    def auto_paging_iter(self):
        page = self

        while True:
            if (
                "ending_before" in self._retrieve_params
                and "starting_after" not in self._retrieve_params
            ):
                for item in reversed(page):
                    yield item
                page = page.previous_page()
            else:
                for item in page:
                    yield item
                page = page.next_page()

            if page.is_empty:
                break

    @classmethod
    def empty_list(
        cls, api_key=None, ten99policy_version=None, ten99policy_environment=None
    ):
        return cls.construct_from(
            {"data": []},
            key=api_key,
            ten99policy_version=ten99policy_version,
            ten99policy_environment=ten99policy_environment,
            last_response=None,
        )

    @property
    def is_empty(self):
        return not self.data

    def next_page(
        self, api_key=None, ten99policy_version=None, ten99policy_environment=None, **params
    ):
        if not self.has_more:
            return self.empty_list(
                api_key=api_key,
                ten99policy_version=ten99policy_version,
                ten99policy_environment=ten99policy_environment,
            )

        last_id = self.data[-1].id

        params_with_filters = self._retrieve_params.copy()
        params_with_filters.update({"starting_after": last_id})
        params_with_filters.update(params)

        return self.list(
            api_key=api_key,
            ten99policy_version=ten99policy_version,
            ten99policy_environment=ten99policy_environment,
            **params_with_filters
        )

    def previous_page(
        self, api_key=None, ten99policy_version=None, **params
    ):
        if not self.has_more:
            return self.empty_list(
                api_key=api_key,
                ten99policy_version=ten99policy_version,
                ten99policy_environment=ten99policy_environment,
            )

        first_id = self.data[0].id

        params_with_filters = self._retrieve_params.copy()
        params_with_filters.update({"ending_before": first_id})
        params_with_filters.update(params)

        return self.list(
            api_key=api_key,
            ten99policy_version=ten99policy_version,
            ten99policy_environment=ten99policy_environment,
            **params_with_filters
        )
