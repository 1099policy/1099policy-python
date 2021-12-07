from __future__ import absolute_import, division, print_function

import functools
import hmac
import io
import logging
import sys
import os
import re

import t99
from t99 import six
from t99.six.moves.urllib.parse import parse_qsl


T99_LOG = os.environ.get("T99_LOG")

logger = logging.getLogger("t99")

__all__ = [
    "io",
    "parse_qsl",
    "utf8",
    "log_info",
    "log_debug",
    "logfmt",
]


def utf8(value):
    if six.PY2 and isinstance(value, six.text_type):
        return value.encode("utf-8")
    else:
        return value


def is_appengine_dev():
    return "APPENGINE_RUNTIME" in os.environ and "Dev" in os.environ.get(
        "SERVER_SOFTWARE", ""
    )


def _console_log_level():
    if t99.log in ["debug", "info"]:
        return t99.log
    elif T99_LOG in ["debug", "info"]:
        return T99_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(dict(message=message, **params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def _test_or_live_environment():
    if t99.api_key is None:
        return
    match = re.match(r"sk_(live|test)_", t99.api_key)
    if match is None:
        return
    return match.groups()[0]


def logfmt(props):
    def fmt(key, val):
        # Handle case where val is a bytes or bytesarray
        if six.PY3 and hasattr(val, "decode"):
            val = val.decode("utf-8")
        # Check if val is already a string to avoid re-encoding into
        # ascii. Since the code is sent through 2to3, we can't just
        # use unicode(val, encoding='utf8') since it will be
        # translated incorrectly.
        if not isinstance(val, six.string_types):
            val = six.text_type(val)
        if re.search(r"\s", val):
            val = repr(val)
        # key should already be a string
        if re.search(r"\s", key):
            key = repr(key)
        return u"{key}={val}".format(key=key, val=val)

    return u" ".join([fmt(key, val) for key, val in sorted(props.items())])


# Borrowed from Django's source code
if hasattr(hmac, "compare_digest"):
    # Prefer the stdlib implementation, when available.
    def secure_compare(val1, val2):
        return hmac.compare_digest(utf8(val1), utf8(val2))


else:

    def secure_compare(val1, val2):
        """
        Returns True if the two strings are equal, False otherwise.
        The time taken is independent of the number of characters that match.
        For the sake of simplicity, this function executes in constant time
        only when the two strings have the same length. It short-circuits when
        they have different lengths.
        """
        val1, val2 = utf8(val1), utf8(val2)
        if len(val1) != len(val2):
            return False
        result = 0
        if six.PY3 and isinstance(val1, bytes) and isinstance(val2, bytes):
            for x, y in zip(val1, val2):
                result |= x ^ y
        else:
            for x, y in zip(val1, val2):
                result |= ord(x) ^ ord(y)
        return result == 0


def get_object_classes():
    # This is here to avoid a circular dependency
    from t99.object_classes import OBJECT_CLASSES

    return OBJECT_CLASSES


def convert_to_t99_object(
    resp, api_key=None, t99_version=None, t99_account=None
):
    # If we get a T99Response, we'll want to return a
    # T99Object with the last_response field filled out with
    # the raw API response information
    t99_response = None

    if isinstance(resp, t99.t99_response.T99Response):
        t99_response = resp
        resp = t99_response.data

    if isinstance(resp, list):
        return [
            convert_to_t99_object(
                i, api_key, t99_version, t99_account
            )
            for i in resp
        ]
    elif isinstance(resp, dict) and not isinstance(
        resp, t99.t99_object.T99Object
    ):
        resp = resp.copy()
        klass_name = resp.get("object")
        if isinstance(klass_name, six.string_types):
            klass = get_object_classes().get(
                klass_name, t99.t99_object.T99Object
            )
        else:
            klass = t99.t99_object.T99Object

        return klass.construct_from(
            resp,
            api_key,
            t99_version=t99_version,
            t99_account=t99_account,
            last_response=t99_response,
        )
    else:
        return resp


def convert_to_dict(obj):
    """Converts a T99Object back to a regular dict.

    Nested T99Objects are also converted back to regular dicts.

    :param obj: The T99Object to convert.

    :returns: The T99Object as a dict.
    """
    if isinstance(obj, list):
        return [convert_to_dict(i) for i in obj]
    # This works by virtue of the fact that T99Objects _are_ dicts. The dict
    # comprehension returns a regular dict and recursively applies the
    # conversion to each value.
    elif isinstance(obj, dict):
        return {k: convert_to_dict(v) for k, v in six.iteritems(obj)}
    else:
        return obj


def populate_headers(idempotency_key):
    if idempotency_key is not None:
        return {"Idempotency-Key": idempotency_key}
    return None


def merge_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z


class class_method_variant(object):
    def __init__(self, class_method_name):
        self.class_method_name = class_method_name

    def __call__(self, method):
        self.method = method
        return self

    def __get__(self, obj, objtype=None):
        @functools.wraps(self.method)
        def _wrapper(*args, **kwargs):
            if obj is not None:
                # Method was called as an instance method, e.g.
                # instance.method(...)
                return self.method(obj, *args, **kwargs)
            elif len(args) > 0 and isinstance(args[0], objtype):
                # Method was called as a class method with the instance as the
                # first argument, e.g. Class.method(instance, ...) which in
                # Python is the same thing as calling an instance method
                return self.method(args[0], *args[1:], **kwargs)
            else:
                # Method was called as a class method, e.g. Class.method(...)
                class_method = getattr(objtype, self.class_method_name)
                return class_method(*args, **kwargs)

        return _wrapper
