from __future__ import absolute_import, division, print_function

import calendar
import datetime
import json
import platform
import time
import uuid
import warnings
from collections import OrderedDict

import ten99policy
from ten99policy import error, http_client, version, util, six
from ten99policy.multipart_data_generator import MultipartDataGenerator
from ten99policy.six.moves.urllib.parse import urlsplit, urlunsplit
from ten99policy.ten99policy_response import TEN99POLICYResponse


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt="%s[%s]"):
    d = OrderedDict()
    for subkey, subvalue in six.iteritems(data):
        d[fmt % (key, subkey)] = subvalue
    return d


def _api_encode(data):
    for key, value in six.iteritems(data):
        key = util.utf8(key)
        if value is None:
            continue
        elif hasattr(value, "ten99policy_id"):
            yield (key, value.ten99policy_id)
        elif isinstance(value, list) or isinstance(value, tuple):
            for i, sv in enumerate(value):
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict("%s[%d]" % (key, i), sv)
                    for k, v in _api_encode(subdict):
                        yield (k, v)
                else:
                    yield ("%s[%d]" % (key, i), util.utf8(sv))
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, util.utf8(value))


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = "%s&%s" % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):
    def __init__(
        self,
        key=None,
        client=None,
        api_base=None,
    ):
        self.api_base = api_base or ten99policy.api_base
        self.api_key = key

        self._default_proxy = None

        from ten99policy import verify_ssl_certs as verify
        from ten99policy import proxy

        if client:
            self._client = client
        elif ten99policy.default_http_client:
            self._client = ten99policy.default_http_client
            if proxy != self._default_proxy:
                warnings.warn(
                    "ten99policy.proxy was updated after sending a "
                    "request - this is a no-op. To use a different proxy, "
                    "set ten99policy.default_http_client to a new client "
                    "configured with the proxy."
                )
        else:
            # If the ten99policy.default_http_client has not been set by the user
            # yet, we'll set it here. This way, we aren't creating a new
            # HttpClient for every request.
            ten99policy.default_http_client = http_client.new_default_http_client(
                verify_ssl_certs=verify, proxy=proxy
            )
            self._client = ten99policy.default_http_client
            self._default_proxy = proxy

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers
        )
        return self.interpret_response(rbody, rcode, rheaders)

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = resp["message"]
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody,
                rcode,
                resp,
            )

        raise self.specific_api_error(
            rbody, rcode, resp, rheaders, error_data
        )

    def specific_api_error(self, rbody, rcode, resp, rheaders, error_data):
        util.log_info(
            "ten99policy API error received",
            error_code=rcode,
            error_message=error_data,
        )

        if rcode == 429:
            return error.RateLimitError(
                error_data, rbody, rcode, resp, rheaders
            )
        elif rcode in [400, 404]:
            if error_data.get("type") == "idempotency_error":
                return error.IdempotencyError(
                    error_data, rbody, rcode, resp, rheaders
                )
            else:
                return error.InvalidRequestError(
                    error_data,
                    error_data.get("param"),
                    error_data.get("code"),
                    rbody,
                    rcode,
                    resp,
                    rheaders,
                )
        elif rcode == 401:
            return error.AuthenticationError(
                error_data, rbody, rcode, resp, rheaders
            )
        elif rcode == 403:
            return error.PermissionError(
                error_data, rbody, rcode, resp, rheaders
            )
        else:
            return error.APIError(
                error_data, rbody, rcode, resp, rheaders
            )

    def request_headers(self, api_key, method):
        user_agent = "TEN99POLICY/v1 PythonBindings/%s" % (version.VERSION,)

        ua = {
            "bindings_version": version.VERSION,
            "lang": "python",
            "publisher": "ten99policy",
            "httplib": self._client.name,
        }
        for attr, func in [
            ["lang_version", platform.python_version],
            ["platform", platform.platform],
            ["uname", lambda: " ".join(platform.uname())],
        ]:
            try:
                val = func()
            except Exception:
                val = "(disabled)"
            ua[attr] = val

        headers = {
            "X-TEN99POLICY-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
            "Authorization": "Bearer %s" % (api_key,),
        }

        if method in ["post", "put", "patch"]:
            headers["Content-Type"] = "application/json"
            headers.setdefault("Idempotency-Key", str(uuid.uuid4()))

        return headers

    def request_raw(
        self,
        method,
        url,
        params=None,
        supplied_headers=None,
    ):
        """
        Mechanism for issuing an API call
        """

        if self.api_key:
            my_api_key = self.api_key
        else:
            my_api_key = ten99policy.api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                "No API key provided. (HINT: set your API key using "
                '"ten99policy.api_key = <API-KEY>"). You can generate API keys '
                "from the TEN99POLICY web interface.  See https://ten99policy.com/api "
                "for details, or email support@ten99policy.com if you have any "
                "questions."
            )

        abs_url = "%s%s" % (self.api_base, url)

        # Don't use strict form encoding by changing the square bracket control
        # characters back to their literals. This is fine by the server, and
        # makes these parameter strings easier to read.
        # encoded_params = json.dumps(dict(_api_encode(params or {})))
        # encoded_params = encoded_params.replace("%5B", "[").replace("%5D", "]")

        encoded_params = json.dumps(params)

        if method == "get" or method == "delete":
            if params:
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == "post" or method == "put" or method == "patch":
            if (
                supplied_headers is not None
                and supplied_headers.get("Content-Type")
                == "multipart/form-data"
            ):
                generator = MultipartDataGenerator()
                generator.add_params(params or {})
                post_data = generator.get_post_data()
                supplied_headers[
                    "Content-Type"
                ] = "multipart/form-data; boundary=%s" % (generator.boundary,)
            else:
                post_data = encoded_params
        else:
            raise error.APIConnectionError(
                "Unrecognized HTTP method %r.  This may indicate a bug in the "
                "TEN99POLICY bindings.  Please contact support@ten99policy.com for "
                "assistance." % (method,)
            )

        headers = self.request_headers(my_api_key, method)
        if supplied_headers is not None:
            for key, value in six.iteritems(supplied_headers):
                headers[key] = value

        util.log_info("Request to TEN99POLICY api", method=method, path=abs_url)
        util.log_debug(
            "Post details",
            post_data=encoded_params,
        )

        rcontent, rcode, rheaders = self._client.request_with_retries(
            method, abs_url, headers, post_data
        )

        util.log_info("TEN99POLICY API response", path=abs_url, response_code=rcode)
        util.log_debug("API response body", body=rcontent)

        return rcontent, rcode, rheaders, my_api_key

    def _should_handle_code_as_error(self, rcode):
        return not 200 <= rcode < 300

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")
            resp = TEN99POLICYResponse(rbody, rcode, rheaders)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody,
                rcode,
                rheaders,
            )
        if self._should_handle_code_as_error(rcode):
            self.handle_error_response(rbody, rcode, resp.data, rheaders)
        return resp
