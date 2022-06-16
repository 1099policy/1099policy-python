# 1099policy Python Library

[![CircleCI](https://circleci.com/gh/1099policy/ten99policy-python/tree/master.svg?style=svg)](https://circleci.com/gh/1099policy/ten99policy-python/tree/master)
[![Maintainability](https://api.codeclimate.com/v1/badges/25dc3b9db072fdfe552e/maintainability)](https://codeclimate.com/github/1099policy/ten99policy-python/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/25dc3b9db072fdfe552e/test_coverage)](https://codeclimate.com/github/1099policy/ten99policy-python/test_coverage)

The 1099policy Python library provides convenient access to the 1099policy API from
applications written in the Python language. It includes a pre-defined set of
classes for API resources that initialize themselves dynamically from API
responses which makes it compatible with a wide range of versions of the 1099policy
API.

## Documentation

See the [Python API docs](https://1099policy.com/docs/api?lang=python).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install --upgrade ten99policy
```

Install from source with:

```sh
python setup.py install
```

### Requirements

-   Python 2.7+ or Python 3.4+ (PyPy supported)

## Usage

The library needs to be configured with your account's secret key which is
available in your [1099policy Dashboard][api-keys]. Set `ten99policy.api_key` to its
value:

```python
import ten99policy
ten99policy.api_key = "sk_test_..."

# list contractors
contractors = ten99policy.Contractors.list()

# print the first contractor's email
print(contractors.data[0].email)

# retrieve specific Contractors
contractor = ten99policy.Contractors.retrieve("cus_123456789")

# print that contractor's email
print(contractor.email)
```

### Handling exceptions

Unsuccessful requests raise exceptions. The class of the exception will reflect
the sort of error that occurred. Please see the [Api
Reference](https://1099policy.com/docs/api/errors/handling) for a description of
the error classes you should handle, and for information on how to inspect
these errors.

### Configuring a Proxy

A proxy can be configured with `ten99policy.proxy`:

```python
ten99policy.proxy = "https://user:pass@example.com:1234"
```

### Configuring Automatic Retries

You can enable automatic retries on requests that fail due to a transient
problem by configuring the maximum number of retries:

```python
ten99policy.max_network_retries = 2
```

Various errors can trigger a retry, like a connection error or a timeout, and
also certain API responses like HTTP status `409 Conflict`.

[Idempotency keys][idempotency-keys] are automatically generated and added to
requests, when not given, to guarantee that retries are safe.

### Logging

The library can be configured to emit logging that will give you better insight
into what it's doing. The `info` logging level is usually most appropriate for
production use, but `debug` is also available for more verbosity.

There are a few options for enabling it:

1. Set the environment variable `TEN99POLICY_LOG` to the value `debug` or `info`

    ```sh
    $ export TEN99POLICY_LOG=debug
    ```

2. Set `ten99policy.log`:

    ```python
    import ten99policy
    ten99policy.log = 'debug'
    ```

3. Enable it through Python's logging module:

    ```python
    import logging
    logging.basicConfig()
    logging.getLogger('ten99policy').setLevel(logging.DEBUG)
    ```
