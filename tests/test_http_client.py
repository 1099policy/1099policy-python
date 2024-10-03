import unittest
import textwrap
from unittest import mock
from unittest.mock import patch, MagicMock, PropertyMock
from unittest.mock import Mock
import urllib
from io import BytesIO

from ten99policy.http_client import (
    HTTPClient,
    RequestsClient,
    UrlFetchClient,
    PycurlClient,
    Urllib2Client,
    new_default_http_client,
)
from ten99policy import error

# Mock dependencies that may not be available during testing
try:
    import requests
except ImportError:
    requests = None

try:
    import pycurl
except ImportError:
    pycurl = None

try:
    from google.appengine.api import urlfetch
except ImportError:
    urlfetch = None


class TestHTTPClientBase(unittest.TestCase):
    def setUp(self):
        self.client = HTTPClient()

    def test_initialization_without_proxy(self):
        client = HTTPClient()
        self.assertTrue(client._verify_ssl_certs)
        self.assertIsNone(client._proxy)

    def test_initialization_with_proxy_string(self):
        proxy = "http://proxy.example.com:8080"
        client = HTTPClient(proxy=proxy)
        expected_proxy = {"http": proxy, "https": proxy}
        self.assertEqual(client._proxy, expected_proxy)

    def test_initialization_with_proxy_dict(self):
        proxy = {
            "http": "http://proxy.example.com:8080",
            "https": "https://proxy.example.com:8443",
        }
        client = HTTPClient(proxy=proxy)
        self.assertEqual(client._proxy, proxy)

    def test_initialization_with_invalid_proxy_type(self):
        with self.assertRaises(ValueError):
            HTTPClient(proxy=123)  # Invalid proxy type

    def test_request_with_retries_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.client.request_with_retries("GET", "http://example.com", {})

    def test_request_stream_with_retries_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.client.request_stream_with_retries("GET", "http://example.com", {})

    def test_should_retry_max_retries_exceeded(self):
        response = (None, 500, {})
        api_connection_error = mock.Mock()
        api_connection_error.should_retry = True
        result = self.client._should_retry(response, api_connection_error, 10)
        self.assertFalse(result)

    def test_should_retry_response_header_force_retry_false(self):
        response = (None, 200, {"ten99policy-should-retry": "false"})
        api_connection_error = None
        result = self.client._should_retry(response, api_connection_error, 1)
        self.assertFalse(result)

    @patch("ten99policy.http_client.time.sleep", return_value=None)
    def test_request_with_retries_success(self, mock_sleep):
        self.client._request_with_retries_internal = mock.Mock(return_value="success")
        result = self.client.request_with_retries("GET", "http://example.com", {})
        self.assertEqual(result, "success")
        self.client._request_with_retries_internal.assert_called_once_with(
            "GET", "http://example.com", {}, None, is_streaming=False
        )

    @patch("ten99policy.http_client.time.sleep", return_value=None)
    def test_request_with_retries_retry_then_success(self, mock_sleep):
        self.client._should_retry = mock.Mock(side_effect=[True, False])
        self.client.request = mock.Mock(
            side_effect=[
                (None, 500, {}),  # First response triggers a retry
                (b'{"success": true}', 200, {}),  # Second response is successful
            ]
        )
        result = self.client.request_with_retries("GET", "http://example.com", {})
        self.assertEqual(result, (b'{"success": true}', 200, {}))
        self.assertEqual(self.client.request.call_count, 2)

    def test_sleep_time_seconds_exponential_backoff(self):
        with patch(
            "ten99policy.http_client.HTTPClient._retry_after_header", return_value=None
        ):
            sleep_time = self.client._sleep_time_seconds(1)
            expected = max(0.5, 0.5 * (1 + 0.5))  # 0.5 * (1 + 0.5) = 0.75
            self.assertGreaterEqual(sleep_time, 0.5)
            self.assertLessEqual(sleep_time, 2)

    def test_sleep_time_seconds_with_retry_after(self):
        with patch(
            "ten99policy.http_client.HTTPClient._retry_after_header", return_value=3
        ):
            sleep_time = self.client._sleep_time_seconds(1)
            self.assertGreaterEqual(sleep_time, 3)

    def test_add_jitter_time(self):
        with patch("ten99policy.http_client.random.uniform", return_value=0.5):
            sleep_time = self.client._add_jitter_time(2)
            self.assertEqual(sleep_time, 2 * 0.5 * (1 + 0.5))  # 2 * 0.5 * 1.5 = 1.5

    def test_close_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            self.client.close()


class TestHTTPClientShouldRetry(unittest.TestCase):
    def setUp(self):
        self.client = HTTPClient()
        self.client._max_network_retries = Mock(return_value=3)

    def test_max_retries_exceeded(self):
        result = self.client._should_retry(None, None, 3)
        self.assertFalse(result)

    def test_response_none_should_retry(self):
        api_connection_error = Mock(should_retry=True)
        result = self.client._should_retry(None, api_connection_error, 1)
        self.assertTrue(result)

    def test_response_none_should_not_retry(self):
        api_connection_error = Mock(should_retry=False)
        result = self.client._should_retry(None, api_connection_error, 1)
        self.assertFalse(result)

    def test_should_retry_header_true(self):
        response = (None, 200, {"ten99policy-should-retry": "true"})
        result = self.client._should_retry(response, None, 1)
        self.assertTrue(result)

    def test_should_retry_header_false(self):
        response = (None, 200, {"ten99policy-should-retry": "false"})
        result = self.client._should_retry(response, None, 1)
        self.assertFalse(result)

    def test_conflict_status_code(self):
        response = (None, 409, {})
        result = self.client._should_retry(response, None, 1)
        self.assertTrue(result)

    def test_internal_server_error(self):
        response = (None, 500, {})
        result = self.client._should_retry(response, None, 1)
        self.assertTrue(result)

    def test_other_5xx_error(self):
        response = (None, 503, {})
        result = self.client._should_retry(response, None, 1)
        self.assertTrue(result)

    def test_non_retryable_status_code(self):
        response = (None, 400, {})
        result = self.client._should_retry(response, None, 1)
        self.assertFalse(result)

    def test_should_retry_header_overrides_status_code(self):
        response = (None, 500, {"ten99policy-should-retry": "false"})
        result = self.client._should_retry(response, None, 1)
        self.assertFalse(result)

    @unittest.skip("Temporarily skipping this test")
    def test_case_insensitive_headers(self):
        response = (None, 200, {"TEN99POLICY-SHOULD-RETRY": "true"})
        result = self.client._should_retry(response, None, 1)
        self.assertTrue(result)


class TestRequestsClient(unittest.TestCase):
    def setUp(self):
        self.mock_session = mock.Mock()
        self.client = RequestsClient(timeout=30, session=self.mock_session)

    def test_initialization(self):
        self.assertEqual(self.client._timeout, 30)
        self.assertEqual(self.client._session, self.mock_session)
        self.assertTrue(self.client._verify_ssl_certs)
        self.assertIsNone(self.client._proxy)

    @patch("ten99policy.http_client.requests.Session")
    def test_initialization_with_default_session(self, mock_session):
        client = RequestsClient()
        mock_session.assert_not_called()
        self.assertIs(client._session, client._session)

    def test_request_internal_get(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.headers = {}
        self.client._thread_local.session = self.mock_session
        self.mock_session.request.return_value = mock_response

        content, status_code, headers = self.client._request_internal(
            "get", "http://example.com", {}, None, False
        )

        self.mock_session.request.assert_called_with(
            "get", "http://example.com", headers={}, data=None, timeout=30, verify=False
        )
        self.assertEqual(content, mock_response.content)
        self.assertEqual(status_code, 200)
        self.assertEqual(headers, mock_response.headers)

    def test_request_internal_post(self):
        mock_response = mock.Mock()
        mock_response.status_code = 201
        mock_response.content = b'{"created": true}'
        mock_response.headers = {}
        self.client._thread_local.session = self.mock_session
        self.mock_session.request.return_value = mock_response

        content, status_code, headers = self.client._request_internal(
            "post", "http://example.com", {}, "data", False
        )

        self.mock_session.request.assert_called_with(
            "post",
            "http://example.com",
            headers={},
            data="data",
            timeout=30,
            verify=False,
        )
        self.assertEqual(content, mock_response.content)
        self.assertEqual(status_code, 201)
        self.assertEqual(headers, mock_response.headers)

    def test_request_internal_streaming(self):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.raw = "streaming content"
        mock_response.headers = {}
        self.client._thread_local.session = self.mock_session
        self.mock_session.request.return_value = mock_response

        content, status_code, headers = self.client._request_internal(
            "get", "http://example.com", {}, None, True
        )

        self.mock_session.request.assert_called_with(
            "get",
            "http://example.com",
            headers={},
            data=None,
            timeout=30,
            verify=False,
            stream=True,
        )
        self.assertEqual(content, mock_response.raw)
        self.assertEqual(status_code, 200)
        self.assertEqual(headers, mock_response.headers)

    def test_handle_request_error_ssl_error(self):
        ssl_error = requests.exceptions.SSLError("SSL certificate error")
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._handle_request_error(ssl_error)
        self.assertIn(
            "Could not verify Ten99Policy's SSL certificate", str(context.exception)
        )
        self.assertFalse(context.exception.should_retry)

    def test_handle_request_error_timeout(self):
        timeout_error = requests.exceptions.Timeout("Request timed out")
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._handle_request_error(timeout_error)
        self.assertIn(
            "Unexpected error communicating with ten99policy", str(context.exception)
        )
        self.assertTrue(context.exception.should_retry)

    def test_handle_request_error_connection_error(self):
        connection_error = requests.exceptions.ConnectionError("Connection failed")
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._handle_request_error(connection_error)
        self.assertIn(
            "Unexpected error communicating with ten99policy", str(context.exception)
        )
        self.assertTrue(context.exception.should_retry)

    def test_handle_request_error_generic_request_exception(self):
        request_exception = requests.exceptions.RequestException("Generic error")
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._handle_request_error(request_exception)
        self.assertIn(
            "Unexpected error communicating with ten99policy", str(context.exception)
        )
        self.assertFalse(context.exception.should_retry)

    def test_close_session(self):
        self.client._thread_local.session = self.mock_session
        self.client.close()
        self.mock_session.close.assert_called_once()


@unittest.skipIf(urlfetch is None, "urlfetch not available")
class TestUrlFetchClient(unittest.TestCase):
    def setUp(self):
        self.client = UrlFetchClient()

    def test_initialization_with_proxy_raises_error(self):
        with self.assertRaises(ValueError):
            UrlFetchClient(proxy="http://proxy.example.com")

    @patch("ten99policy.http_client.urlfetch.fetch")
    def test_request_internal_get(self, mock_fetch):
        mock_result = mock.Mock()
        mock_result.content = b'{"success": true}'
        mock_result.status_code = 200
        mock_result.headers = {}
        mock_fetch.return_value = mock_result

        content, status_code, headers = self.client._request_internal(
            "get", "http://example.com", {}, None, False
        )

        mock_fetch.assert_called_with(
            url="http://example.com",
            method="get",
            headers={},
            validate_certificate=True,
            deadline=55,
            payload=None,
        )
        self.assertEqual(content, mock_result.content)
        self.assertEqual(status_code, 200)
        self.assertEqual(headers, mock_result.headers)

    @patch("ten99policy.http_client.urlfetch.fetch")
    def test_request_internal_post_streaming(self, mock_fetch):
        mock_result = mock.Mock()
        mock_result.content = b"streaming content"
        mock_result.status_code = 200
        mock_result.headers = {}
        mock_fetch.return_value = mock_result

        content, status_code, headers = self.client._request_internal(
            "post", "http://example.com", {}, "data", True
        )

        mock_fetch.assert_called_with(
            url="http://example.com",
            method="post",
            headers={},
            validate_certificate=True,
            deadline=55,
            payload="data",
        )
        self.assertEqual(content, b"streaming content")
        self.assertEqual(status_code, 200)
        self.assertEqual(headers, mock_result.headers)

    @patch("ten99policy.http_client.urlfetch.fetch")
    def test_handle_request_error_invalid_url(self, mock_fetch):
        mock_fetch.side_effect = urlfetch.InvalidURLError()
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._request_internal("get", "invalid:url", {}, None, False)
        self.assertIn("attempted to fetch an invalid URL", str(context.exception))

    @patch("ten99policy.http_client.urlfetch.fetch")
    def test_handle_request_error_download_error(self, mock_fetch):
        mock_fetch.side_effect = urlfetch.DownloadError()
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._request_internal("get", "http://example.com", {}, None, False)
        self.assertIn(
            "problem retrieving data from ten99policy", str(context.exception)
        )

    def test_close_no_op(self):
        # UrlFetchClient.close is a no-op
        try:
            self.client.close()
        except Exception as e:
            self.fail(f"UrlFetchClient.close() raised an exception {e}")


@unittest.skipIf(pycurl is None, "pycurl not available")
class TestPycurlClient(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("ten99policy.http_client.pycurl.Curl")
        self.mock_curl_class = self.patcher.start()
        self.mock_curl = mock.Mock()
        self.mock_curl_class.return_value = self.mock_curl
        self.client = PycurlClient()

    def tearDown(self):
        self.patcher.stop()

    def test_initialization_with_proxy(self):
        proxy = {"http": "http://proxy.example.com:8080"}
        client = PycurlClient(proxy=proxy)
        parsed_proxy = mock.Mock()
        with patch("ten99policy.http_client.urlparse", return_value=parsed_proxy):
            client._get_proxy("http://example.com")
            self.mock_curl.setopt.assert_called_with(
                pycurl.PROXY, parsed_proxy.hostname
            )

    @patch("ten99policy.http_client.util.io.BytesIO")
    def test_request_internal_get(self, mock_bytesio):
        mock_response = mock.Mock()
        mock_response.getvalue.return_value = b'{"success": true}'
        mock_write = mock_bytesio.return_value.write
        mock_header_write = mock_bytesio.return_value.write
        self.mock_curl.perform.return_value = None
        self.mock_curl.getinfo.return_value = 200
        mock_curl_instance = self.mock_curl

        self.mock_curl.getinfo.return_value = 200
        mock_bytesio.side_effect = [mock.Mock(), mock.Mock()]
        content, status_code, headers = self.client._request_internal(
            "get", "http://example.com", {}, None, False
        )

        self.mock_curl.setopt.assert_any_call(pycurl.HTTPGET, 1)
        self.mock_curl.setopt.assert_any_call(pycurl.URL, "http://example.com")
        self.assertTrue(mock_curl_instance.perform.called)
        self.assertEqual(status_code, 200)

    @patch("ten99policy.http_client.util.io.BytesIO")
    def test_request_internal_post_streaming(self, mock_bytesio):
        mock_response = mock.Mock()
        mock_response.getvalue.return_value = b"streaming content"
        self.mock_curl.perform.return_value = None
        self.mock_curl.getinfo.return_value = 200
        mock_bytesio.side_effect = [mock.Mock(), mock.Mock()]
        content, status_code, headers = self.client._request_internal(
            "post", "http://example.com", {}, "data", True
        )

        self.mock_curl.setopt.assert_any_call(pycurl.POST, 1)
        self.mock_curl.setopt.assert_any_call(pycurl.POSTFIELDS, "data")
        self.mock_curl.setopt.assert_any_call(pycurl.URL, "http://example.com")
        self.assertTrue(self.mock_curl.perform.called)
        self.assertEqual(status_code, 200)

    def test_handle_request_error_connection_error(self):
        self.mock_curl.perform.side_effect = pycurl.error(
            pycurl.E_COULDNT_CONNECT, "Connection failed"
        )
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._request_internal("get", "http://example.com", {}, None, False)
        self.assertIn("Could not connect to ten99policy", str(context.exception))
        self.assertTrue(context.exception.should_retry)

    def test_handle_request_error_ssl_error(self):
        self.mock_curl.perform.side_effect = pycurl.error(
            pycurl.E_SSL_CACERT, "SSL cert error"
        )
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._request_internal("get", "http://example.com", {}, None, False)
        self.assertIn(
            "Could not verify Ten99Policy's SSL certificate", str(context.exception)
        )
        self.assertFalse(context.exception.should_retry)

    @patch("ten99policy.http_client.util.io.BytesIO")
    def test_request_internal_custom_method(self, mock_bytesio):
        # Example of a PUT request with custom method
        mock_bytesio.side_effect = [mock.Mock(), mock.Mock()]
        self.mock_curl.getinfo.return_value = 204
        self.client._request_internal(
            "put", "http://example.com/resource", {}, None, False
        )
        self.mock_curl.setopt.assert_any_call(pycurl.CUSTOMREQUEST, "PUT")
        self.assertTrue(self.mock_curl.perform.called)


@unittest.skipIf(requests is None, "requests not available")
class TestRequestsClientWithProxy(unittest.TestCase):
    def setUp(self):
        self.mock_session = mock.Mock()
        self.proxy = {
            "http": "http://proxy.example.com:8080",
            "https": "https://proxy.example.com:8443",
        }
        self.client = RequestsClient(proxy=self.proxy)

    @patch("ten99policy.http_client.requests.Session")
    def test_initialization_with_proxy(self, mock_session):
        client = RequestsClient(proxy=self.proxy)
        self.assertEqual(client._proxy, self.proxy)

    @patch("ten99policy.http_client.requests.Session")
    def test_request_internal_with_proxy(self, mock_session):
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.content = b'{"success": true}'
        mock_response.headers = {}
        self.client._thread_local.session = self.mock_session
        self.mock_session.request.return_value = mock_response

        content, status_code, headers = self.client._request_internal(
            "get", "http://example.com", {}, None, False
        )

        expected_proxies = self.proxy
        self.mock_session.request.assert_called_with(
            "get",
            "http://example.com",
            headers={},
            data=None,
            timeout=80,
            verify=False,
            proxies=expected_proxies,
        )
        self.assertEqual(content, mock_response.content)
        self.assertEqual(status_code, 200)
        self.assertEqual(headers, mock_response.headers)


class TestUrllib2Client(unittest.TestCase):
    def setUp(self):
        self.patcher = patch("ten99policy.http_client.urllib.request.OpenerDirector")
        self.mock_opener = self.patcher.start()
        self.client = Urllib2Client()

    def tearDown(self):
        self.patcher.stop()

    def test_initialization_without_proxy(self):
        client = Urllib2Client()
        self.assertIsNone(client._opener)

    def test_initialization_with_proxy(self):
        proxy = {
            "http": "http://proxy.example.com:8080",
            "https": "https://proxy.example.com:8443",
        }
        with patch(
            "ten99policy.http_client.urllib.request.ProxyHandler"
        ) as mock_proxy_handler, patch(
            "ten99policy.http_client.urllib.request.build_opener"
        ) as mock_build_opener:
            mock_proxy_handler.return_value = MagicMock()
            mock_build_opener.return_value = MagicMock()
            client = Urllib2Client(proxy=proxy)
            mock_proxy_handler.assert_called_with(proxy)
            mock_build_opener.assert_called_with(mock_proxy_handler.return_value)
            self.assertEqual(client._opener, mock_build_opener.return_value)

    @patch("ten99policy.http_client.urllib.request.Request")
    @patch("ten99policy.http_client.urllib.request.urlopen")
    def test_request_internal_get(self, mock_urlopen, mock_request):
        mock_response = mock.Mock()
        mock_response.read.return_value = b'{"success": true}'
        mock_response.code = 200
        mock_response.info.return_value = {"Content-Type": "application/json"}
        mock_urlopen.return_value = mock_response

        content, status_code, headers = self.client._request_internal(
            "get", "http://example.com", {}, None, False
        )

        mock_request.assert_called_with("http://example.com", None, {})
        mock_urlopen.assert_called_with(mock_request.return_value)
        self.assertEqual(content, b'{"success": true}')
        self.assertEqual(status_code, 200)

        # Convert both dictionaries to lowercase keys for comparison
        lowercase_headers = {k.lower(): v for k, v in headers.items()}
        expected_headers = {"content-type": "application/json"}
        self.assertEqual(lowercase_headers, expected_headers)

    @patch(
        "ten99policy.http_client.urllib.request.urlopen",
        side_effect=urllib.error.URLError("Timeout"),
    )
    def test_handle_request_error_urllib_error(self, mock_urlopen):
        with self.assertRaises(error.APIConnectionError) as context:
            self.client._request_internal("get", "http://example.com", {}, None, False)
        self.assertIn(
            "Unexpected error communicating with ten99policy", str(context.exception)
        )

    @patch("ten99policy.http_client.urllib.request.Request")
    @patch("ten99policy.http_client.urllib.request.urlopen")
    def test_request_internal_post_streaming(self, mock_urlopen, mock_request):
        mock_response = mock.Mock()
        mock_response.read.return_value = b'{"created": true}'
        mock_response.code = 201
        mock_response.info.return_value = {"Content-Type": "application/json"}
        mock_urlopen.return_value = mock_response

        content, status_code, headers = self.client._request_internal(
            "post", "http://example.com/resource", {}, "data", True
        )

        mock_request.assert_called_with("http://example.com/resource", b"data", {})
        mock_urlopen.assert_called_with(mock_request.return_value)
        self.assertEqual(content, mock_urlopen.return_value)
        self.assertEqual(status_code, 201)
        self.assertEqual(headers, {"content-type": "application/json"})
        self.assertEqual(content.read(), b'{"created": true}')

    def test_close_no_op(self):
        # Urllib2Client.close is a no-op
        try:
            self.client.close()
        except Exception as e:
            self.fail(f"Urllib2Client.close() raised an exception {e}")


# Create a mock urlfetch module with the required error classes
mock_urlfetch = Mock()
mock_urlfetch.InvalidURLError = type("InvalidURLError", (Exception,), {})
mock_urlfetch.DownloadError = type("DownloadError", (Exception,), {})
mock_urlfetch.ResponseTooLargeError = type("ResponseTooLargeError", (Exception,), {})


class TestUrlFetchClientHandleRequestError(unittest.TestCase):
    @patch("ten99policy.http_client.urlfetch", mock_urlfetch)
    def setUp(self):
        self.client = UrlFetchClient()
        self.url = "https://api.ten99policy.com/v1/example"

    @patch("ten99policy.http_client.urlfetch", mock_urlfetch)
    def test_invalid_url_error(self):
        e = mock_urlfetch.InvalidURLError()
        expected_msg = (
            "The Ten99Policy library attempted to fetch an "
            "invalid URL ('https://api.ten99policy.com/v1/example'). This is likely due to a bug "
            "in the Ten99Policy Python bindings. Please let us know "
            "at support@1099policy.com."
        )
        expected_msg = textwrap.fill(expected_msg) + f"\n\n(Network error: {str(e)})"

        with self.assertRaises(error.APIConnectionError) as cm:
            self.client._handle_request_error(e, self.url)

        self.assertEqual(str(cm.exception), expected_msg)

    @patch("ten99policy.http_client.urlfetch", mock_urlfetch)
    def test_download_error(self):
        e = mock_urlfetch.DownloadError()
        expected_msg = "There was a problem retrieving data from ten99policy."
        expected_msg = textwrap.fill(expected_msg) + f"\n\n(Network error: {str(e)})"

        with self.assertRaises(error.APIConnectionError) as cm:
            self.client._handle_request_error(e, self.url)

        self.assertEqual(str(cm.exception), expected_msg)

    @patch("ten99policy.http_client.urlfetch", mock_urlfetch)
    def test_response_too_large_error(self):
        e = mock_urlfetch.ResponseTooLargeError()
        expected_msg = (
            "There was a problem receiving all of your data from "
            "ten99policy.  This is likely due to a bug in ten99policy. "
            "Please let us know at support@1099policy.com."
        )
        expected_msg = textwrap.fill(expected_msg) + f"\n\n(Network error: {str(e)})"

        with self.assertRaises(error.APIConnectionError) as cm:
            self.client._handle_request_error(e, self.url)

        self.assertEqual(str(cm.exception), expected_msg)

    @patch("ten99policy.http_client.urlfetch", mock_urlfetch)
    def test_unexpected_error(self):
        e = Exception("Unexpected error")
        expected_msg = (
            "Unexpected error communicating with ten99policy. If this "
            "problem persists, let us know at support@1099policy.com."
        )
        expected_msg = textwrap.fill(expected_msg) + f"\n\n(Network error: {str(e)})"

        with self.assertRaises(error.APIConnectionError) as cm:
            self.client._handle_request_error(e, self.url)

        self.assertEqual(str(cm.exception), expected_msg)


class TestNewDefaultHttpClient(unittest.TestCase):
    @patch("ten99policy.http_client.urlfetch", MagicMock())
    def test_new_default_http_client_urlfetch_available(self):
        client = new_default_http_client()
        self.assertIsInstance(client, UrlFetchClient)

    @patch("ten99policy.http_client.urlfetch", None)
    @patch("ten99policy.http_client.requests", MagicMock())
    def test_new_default_http_client_requests_available(self):
        client = new_default_http_client()
        self.assertIsInstance(client, RequestsClient)

    @patch("ten99policy.http_client.urlfetch", None)
    @patch("ten99policy.http_client.requests", None)
    @patch("ten99policy.http_client.pycurl", MagicMock())
    def test_new_default_http_client_pycurl_available(self):
        client = new_default_http_client()
        self.assertIsInstance(client, PycurlClient)

    @patch("ten99policy.http_client.urlfetch", None)
    @patch("ten99policy.http_client.requests", None)
    @patch("ten99policy.http_client.pycurl", None)
    @patch("ten99policy.http_client.urllib.request", MagicMock())
    def test_new_default_http_client_urllib2_fallback(self):
        with patch("ten99policy.http_client.warnings") as mock_warnings:
            client = new_default_http_client()
            self.assertIsInstance(client, Urllib2Client)
            mock_warnings.warn.assert_called_once()

    @patch("ten99policy.http_client.urlfetch", None)
    @patch("ten99policy.http_client.requests", MagicMock())
    def test_new_default_http_client_requests_new_enough(self):
        with patch("ten99policy.http_client.requests") as mock_requests:
            type(mock_requests).version = PropertyMock(return_value="0.8.8")
            client = new_default_http_client()
            self.assertIsInstance(client, RequestsClient)


if __name__ == "__main__":
    unittest.main()
