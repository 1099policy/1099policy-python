from __future__ import absolute_import, division, print_function

import atexit
import os
import sys
from distutils.version import StrictVersion

import pytest

import t99
from t99.six.moves.urllib.request import urlopen
from t99.six.moves.urllib.error import HTTPError

from tests.request_mock import RequestMock
from tests.t99_mock import T99Mock

MOCK_MINIMUM_VERSION = "0.109.0"

# Starts t99-mock if an OpenAPI spec override is found in `openapi/`, and
# otherwise fall back to `T99_MOCK_PORT` or 12111.
if T99Mock.start():
    MOCK_PORT = T99Mock.port()
else:
    MOCK_PORT = os.environ.get("T99_MOCK_PORT", 12111)


@atexit.register
def stop_t99_mock():
    T99Mock.stop()


def pytest_configure(config):
    if not config.getoption("--nomock"):
        try:
            resp = urlopen("http://localhost:%s/" % MOCK_PORT)
            info = resp.info()
            version = info.get("T99-Mock-Version")
            if version != "master" and StrictVersion(version) < StrictVersion(
                MOCK_MINIMUM_VERSION
            ):
                sys.exit(
                    "Your version of t99-mock (%s) is too old. The minimum "
                    "version to run this test suite is %s. Please "
                    "see its repository for upgrade instructions."
                    % (version, MOCK_MINIMUM_VERSION)
                )

        except HTTPError as e:
            info = e.info()
        except Exception:
            sys.exit(
                "Couldn't reach t99-mock at `localhost:%s`. Is "
                "it running? Please see README for setup instructions."
                % MOCK_PORT
            )


def pytest_addoption(parser):
    parser.addoption(
        "--nomock",
        action="store_true",
        help="only run tests that don't need t99-mock",
    )


def pytest_runtest_setup(item):
    if "request_mock" in item.fixturenames and item.config.getoption(
        "--nomock"
    ):
        pytest.skip(
            "run t99-mock locally and remove --nomock flag to run skipped tests"
        )


@pytest.fixture(autouse=True)
def setup_t99():
    orig_attrs = {
        "api_base": t99.api_base,
        "api_key": t99.api_key,
        "client_id": t99.client_id,
        "default_http_client": t99.default_http_client,
    }
    http_client = t99.http_client.new_default_http_client()
    t99.api_base = "http://localhost:%s" % MOCK_PORT
    t99.api_key = "sk_test_123"
    t99.client_id = "ca_123"
    t99.default_http_client = http_client
    yield
    http_client.close()
    t99.api_base = orig_attrs["api_base"]
    t99.api_key = orig_attrs["api_key"]
    t99.client_id = orig_attrs["client_id"]
    t99.default_http_client = orig_attrs["default_http_client"]


@pytest.fixture
def request_mock(mocker):
    return RequestMock(mocker)
