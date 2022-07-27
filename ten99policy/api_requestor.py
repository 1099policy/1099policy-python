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
from ten99policy.ten99policy_response import Ten99PolicyResponse, Ten99PolicyStreamResponse


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
        api_version=None,
        environment=None,
    ):
        self.api_base = api_base or ten99policy.api_base
        self.api_key = key
        self.api_version = api_version or ten99policy.api_version
        self.ten99policy_environment = environment or ten99policy.environment

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
            method.lower(), url, params, headers, is_streaming=False
        )
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, my_api_key

    def request_stream(self, method, url, params=None, headers=None):
        stream, rcode, rheaders, my_api_key = self.request_raw(
            method.lower(), url, params, headers, is_streaming=True
        )
        resp = self.interpret_streaming_response(stream, rcode, rheaders)
        return resp, my_api_key

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = resp["error"]
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r (HTTP response code "
                "was %d)" % (rbody, rcode),
                rbody,
                rcode,
                resp,
            )

        err = None

        if err is None:
            err = self.specific_api_error(
                rbody, rcode, resp, rheaders, error_data
            )

        raise err

    def specific_api_error(self, rbody, rcode, resp, rheaders, error_data):
        # CFK: take a look at here
        util.log_info("Ten99Policy API error received", error_message=error_data)
        return error.Ten99PolicyError(
            error_data, rbody, rcode, resp, rheaders
        )

    def request_headers(self, api_key, method):
        user_agent = "Ten99Policy/v1 PythonBindings/%s" % (version.VERSION,)

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
            "X-Ten99Policy-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
            "Authorization": "Bearer %s" % (api_key,),
        }

        if self.ten99policy_environment:
            headers["Ten99Policy-Environment"] = self.ten99policy_environment

        if method in ["post", "put", "patch"]:
            headers["Content-Type"] = "application/json"
            headers.setdefault("Idempotency-Key", str(uuid.uuid4()))

        if self.api_version is not None:
            headers["Ten99Policy-Version"] = self.api_version

        return headers

    def request_raw(
        self,
        method,
        url,
        params=None,
        supplied_headers=None,
        is_streaming=False,
    ):
        """
        Mechanism for issuing an API call
        """

        if self.api_key:
            my_api_key = self.api_key
        else:
            from ten99policy import api_key

            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                "No API key provided. (HINT: set your API key using "
                '"ten99policy.api_key = <API-KEY>"). You can generate API keys '
                "from the Ten99Policy web interface.  See https://1099policy.com/api "
                "for details, or email support@1099policy.com if you have any "
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
                "Ten99Policy bindings.  Please contact support@1099policy.com for "
                "assistance." % (method,)
            )

        headers = self.request_headers(my_api_key, method)
        if supplied_headers is not None:
            for key, value in six.iteritems(supplied_headers):
                headers[key] = value

        util.log_info("Request to Ten99Policy api", method=method, path=abs_url)
        util.log_debug(
            "Post details",
            post_data=encoded_params,
            api_version=self.api_version,
        )

        if is_streaming:
            (
                rcontent,
                rcode,
                rheaders,
            ) = self._client.request_stream_with_retries(
                method, abs_url, headers, post_data
            )
        else:
            rcontent, rcode, rheaders = self._client.request_with_retries(
                method, abs_url, headers, post_data
            )

        util.log_info("Ten99Policy API response", path=abs_url, response_code=rcode)
        util.log_debug("API response body", body=rcontent)

        return rcontent, rcode, rheaders, my_api_key

    def _should_handle_code_as_error(self, rcode):
        return not 200 <= rcode < 300

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")
            resp = Ten99PolicyResponse(rbody, rcode, rheaders)
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

    def interpret_streaming_response(self, stream, rcode, rheaders):
        # Streaming response are handled with minimal processing for the success
        # case (ie. we don't want to read the content). When an error is
        # received, we need to read from the stream and parse the received JSON,
        # treating it like a standard JSON response.
        if self._should_handle_code_as_error(rcode):
            if hasattr(stream, "getvalue"):
                json_content = stream.getvalue()
            elif hasattr(stream, "read"):
                json_content = stream.read()
            else:
                raise NotImplementedError(
                    "HTTP client %s does not return an IOBase object which "
                    "can be consumed when streaming a response."
                )

            return self.interpret_response(json_content, rcode, rheaders)
        else:
            return Ten99PolicyStreamResponse(stream, rcode, rheaders)
