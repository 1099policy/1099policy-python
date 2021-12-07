from __future__ import absolute_import, division, print_function

from t99 import api_requestor, error, util, six
from t99.t99_object import T99Object
from t99.six.moves.urllib.parse import quote_plus


class APIResource(T99Object):
    @classmethod
    def retrieve(cls, id, api_key=None, **params):
        instance = cls(id, api_key, **params)
        instance.refresh()
        return instance

    def refresh(self):
        self.refresh_from(self.request("get", self.instance_url()))
        return self

    @classmethod
    def class_url(cls):
        if cls == APIResource:
            raise NotImplementedError(
                "APIResource is an abstract class.  You should perform "
                "actions on its subclasses (e.g. Charge, Customer)"
            )
        # Namespaces are separated in object names with periods (.) and in URLs
        # with forward slashes (/), so replace the former with the latter.
        base = cls.OBJECT_NAME.replace(".", "/")
        return "/api/v1/%s" % (base,)

    def instance_url(self):
        id = self.get("id")

        if not isinstance(id, six.string_types):
            raise error.InvalidRequestError(
                "Could not determine which URL to request: %s instance "
                "has invalid ID: %r, %s. ID should be of type `str` (or"
                " `unicode`)" % (type(self).__name__, id, type(id)),
                "id",
            )

        id = util.utf8(id)
        base = self.class_url()
        extn = quote_plus(id)
        return "%s/%s" % (base, extn)

    # The `method_` and `url_` arguments are suffixed with an underscore to
    # avoid conflicting with actual request parameters in `params`.
    @classmethod
    def _static_request(
        cls,
        method_,
        url_,
        api_key=None,
        idempotency_key=None,
        t99_version=None,
        t99_account=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key, api_version=t99_version, account=t99_account
        )
        headers = util.populate_headers(idempotency_key)
        response, api_key = requestor.request(method_, url_, params, headers)
        return util.convert_to_t99_object(
            response, api_key, t99_version, t99_account
        )

    # The `method_` and `url_` arguments are suffixed with an underscore to
    # avoid conflicting with actual request parameters in `params`.
    @classmethod
    def _static_request_stream(
        cls,
        method_,
        url_,
        api_key=None,
        idempotency_key=None,
        t99_version=None,
        t99_account=None,
        **params
    ):
        requestor = api_requestor.APIRequestor(
            api_key, api_version=t99_version, account=t99_account
        )
        headers = util.populate_headers(idempotency_key)
        response, _ = requestor.request_stream(method_, url_, params, headers)
        return response
