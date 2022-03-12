from __future__ import absolute_import, division, print_function

import ten99policy
from ten99policy.six import python_2_unicode_compatible


@python_2_unicode_compatible
class TEN99POLICYError(Exception):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super(TEN99POLICYError, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = (
                    "<Could not decode body as utf-8. "
                    "Please report to support@ten99policy.com>"
                )

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.request_id = self.headers.get("request-id", None)
        self.error = self.construct_error_object()

    def __str__(self):
        msg = self._message or "<empty message>"
        if self.request_id is not None:
            return u"Request {0}: {1}".format(self.request_id, msg)
        else:
            return msg

    # Returns the underlying `Exception` (base class) message, which is usually
    # the raw message returned by TEN99POLICY's API. This was previously available
    # in python2 via `error.message`. Unlike `str(error)`, it omits "Request
    # req_..." from the beginning of the string.
    @property
    def user_message(self):
        return self._message

    def __repr__(self):
        return "%s(message=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.http_status,
            self.request_id,
        )

    def construct_error_object(self):
        if (
            self.json_body is None
            or "message" not in self.json_body
            or not isinstance(self.json_body["message"], dict)
        ):
            return None

        return self


class APIError(TEN99POLICYError):
    pass


class APIConnectionError(TEN99POLICYError):
    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        super(APIConnectionError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )
        self.should_retry = should_retry


class TEN99POLICYErrorWithParamCode(TEN99POLICYError):
    def __repr__(self):
        return (
            "%s(message=%r, param=%r, code=%r, http_status=%r, "
            "request_id=%r)"
            % (
                self.__class__.__name__,
                self._message,
                self.param,
                self.code,
                self.http_status,
                self.request_id,
            )
        )


class IdempotencyError(TEN99POLICYError):
    pass


class InvalidRequestError(TEN99POLICYErrorWithParamCode):
    def __init__(
        self,
        message,
        param,
        code=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
    ):
        super(InvalidRequestError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )
        self.param = param


class AuthenticationError(TEN99POLICYError):
    pass


class PermissionError(TEN99POLICYError):
    pass


class RateLimitError(TEN99POLICYError):
    pass

