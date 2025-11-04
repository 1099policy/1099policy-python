# ten99policy Python Library

A Python library for interacting with the 1099Policy API.

[![Python Tests](https://github.com/1099policy/1099policy-python/actions/workflows/python-tests.yml/badge.svg)](https://github.com/1099policy/1099policy-python/actions/workflows/python-tests.yml)
[![PyPI version](https://badge.fury.io/py/ten99policy.svg)](https://badge.fury.io/py/ten99policy)
[![Python Versions](https://img.shields.io/pypi/pyversions/ten99policy.svg)](https://pypi.org/project/ten99policy/)

## Overview

The `ten99policy` library provides a simple and intuitive way to integrate 1099Policy's services into your Python applications. It allows you to manage entities, contractors, jobs, policies, quotes, assignments, and more through the 1099Policy API.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Entities](#entities)
    - [Creating an Entity](#creating-an-entity)
    - [Updating an Entity](#updating-an-entity)
    - [Fetching the List of Entities](#fetching-the-list-of-entities)
    - [Retrieving an Entity](#retrieving-an-entity)
    - [Deleting an Entity](#deleting-an-entity)
  - [Contractors](#contractors)
    - [Creating a Contractor](#creating-a-contractor)
    - [Updating a Contractor](#updating-a-contractor)
    - [Fetching the List of Contractors](#fetching-the-list-of-contractors)
    - [Retrieving a Contractor](#retrieving-a-contractor)
    - [Deleting a Contractor](#deleting-a-contractor)
  - [Insurance Application Sessions](#insurance-application-sessions)
    - [Creating an Insurance Application Session](#creating-an-insurance-application-session)
    - [Updating a Session](#updating-a-session)
    - [Fetching the List of Insurance Application Sessions](#fetching-the-list-of-insurance-application-sessions)
    - [Retrieving an Insurance Application Session](#retrieving-an-insurance-application-session)
  - [Jobs](#jobs)
    - [Creating a Job](#creating-a-job)
    - [Updating a Job](#updating-a-job)
    - [Fetching the List of Jobs](#fetching-the-list-of-jobs)
    - [Retrieving a Job](#retrieving-a-job)
    - [Deleting a Job](#deleting-a-job)
  - [Policies](#policies)
    - [Creating a Policy](#creating-a-policy)
    - [Updating a Policy](#updating-a-policy)
    - [Fetching the List of Policies](#fetching-the-list-of-policies)
    - [Retrieving a Policy](#retrieving-a-policy)
    - [Deleting a Policy](#deleting-a-policy)
  - [Quotes](#quotes)
    - [Creating a Quote](#creating-a-quote)
    - [Updating a Quote](#updating-a-quote)
    - [Fetching the List of Quotes](#fetching-the-list-of-quotes)
    - [Retrieving a Quote](#retrieving-a-quote)
  - [Assignments](#assignments)
    - [Creating an Assignment](#creating-an-assignment)
    - [Updating an Assignment](#updating-an-assignment)
    - [Fetching the List of Assignments](#fetching-the-list-of-assignments)
    - [Retrieving an Assignment](#retrieving-an-assignment)
    - [Deleting an Assignment](#deleting-an-assignment)
- [Error Handling](#error-handling)
- [Additional Resources](#additional-resources)
- [Support](#support)
- [License](#license)

## Installation

Install the package using `pip`:

```bash
pip install ten99policy
```

## Configuration

Before using the library, configure it with your API credentials and settings.

```python
import ten99policy

# Configuration variables
ten99policy.api_key = 'your_api_key_here'
ten99policy.environment = 'production'  # or 'sandbox' for testing
ten99policy.api_base = 'https://api.1099policy.com'  # Default API base URL
ten99policy.verify_ssl_certs = True  # Set to False if you encounter SSL issues
ten99policy.log = 'debug'  # Logging level ('debug' or 'info')
```

**Configuration Parameters:**

- `api_key`: Your API key for authentication.
- `environment`: The API environment to use (`'production'` or `'sandbox'`).
- `api_base`: The base URL for API requests.
- `verify_ssl_certs`: Whether to verify SSL certificates.
- `log`: Logging level for console output (`'debug'` or `'info'`).

## Usage

### Entities

#### Creating an Entity

```python
import ten99policy

resource = ten99policy.Entities.create(
    name="Brooklyn Bowl",
    coverage_limit={
        "aggregate_limit": "200000000",
        "occurrence_limit": "100000000",
    },
    address={
        "line1": "3639 18th St",
        "line2": "",
        "locality": "San Francisco",
        "region": "CA",
        "postalcode": "94110",
    },
    required_coverage=["general", "workers-comp"],
)
```

#### Updating an Entity

```python
resource = ten99policy.Entities.modify(
    "en_C9Z2DmfHSF",  # Replace with an existing entity ID
    name="California Roll",
)
```

#### Fetching the List of Entities

```python
resource = ten99policy.Entities.list()
```

#### Retrieving an Entity

```python
resource = ten99policy.Entities.retrieve("en_BUcNa8jMrq")  # Replace with an existing entity ID
```

#### Deleting an Entity

```python
resource = ten99policy.Entities.delete("en_C9Z2DmfHSF")  # Replace with an existing entity ID
```

---

### Contractors

#### Creating a Contractor

```python
resource = ten99policy.Contractors.create(
    first_name="John",
    last_name="Doe",
    email="john@doe.com",
    phone="415-111-1111",
    tax_identification="123-456789",
    address={
        "country": "USA",
        "line1": "2211 Mission St",
        "locality": "San Francisco",
        "region": "CA",
        "postalcode": "94110",
    },
)
```

#### Updating a Contractor

```python
resource = ten99policy.Contractors.modify(
    "cn_tS3wR3UQ5q",  # Replace with an existing contractor ID
    email="john.doe@gmail.com",
    first_name="George",
)
```

#### Fetching the List of Contractors

```python
resource = ten99policy.Contractors.list()
```

#### Retrieving a Contractor

```python
resource = ten99policy.Contractors.retrieve("cn_9TPKz6B9so")  # Replace with an existing contractor ID
```

#### Deleting a Contractor

```python
resource = ten99policy.Contractors.delete("cn_tS3wR3UQ5q")  # Replace with an existing contractor ID
```

---

### Insurance Application Sessions

#### Creating an Insurance Application Session

```python
resource = ten99policy.InsuranceApplicationSessions.create(
    quote="qt_yVEnbNaWh6",
    success_url="http://example.com/success",
    cancel_url="http://example.com/cancel",
)
```

#### Updating a Session

```python
resource = ten99policy.InsuranceApplicationSessions.modify(
    "ias_01HZSB299T5D9SCNY98T8P10KC",  # Replace with an existing session ID
    success_url="http://example.com/success",
    cancel_url="http://example.com/cancel",
)
```

#### Fetching the List of Insurance Application Sessions

```python
resource = ten99policy.InsuranceApplicationSessions.list()
```

#### Retrieving an Insurance Application Session

```python
resource = ten99policy.InsuranceApplicationSessions.retrieve(
    "ias_01HZSB299T5D9SCNY98T8P10KC"  # Replace with an existing session ID
)
```

---

### Jobs

#### Creating a Job

```python
resource = ten99policy.Jobs.create(
    name="Truck driver",
    description="Requires a truck",
    duration_hours=20,
    wage=100,
    years_experience=20,
    wage_type="flatfee",
    entity="en_FwZfQRe4aW",
    category_code="jc_MTqpkbkp6G",
)
```

#### Updating a Job

```python
resource = ten99policy.Jobs.modify(
    "jb_C9Z2DmfHSF",  # Replace with an existing job ID
    name="Mechanic",
)
```

#### Fetching the List of Jobs

```python
resource = ten99policy.Jobs.list()
```

#### Retrieving a Job

```python
resource = ten99policy.Jobs.retrieve("jb_C9Z2DmfHSF")  # Replace with an existing job ID
```

#### Deleting a Job

```python
resource = ten99policy.Jobs.delete("jb_C9Z2DmfHSF")  # Replace with an existing job ID
```

---

### Policies

#### Creating a Policy

```python
resource = ten99policy.Policies.create(
    quote_id="qt_UPmEfS6nNK",
    is_active=True,
)
```

#### Updating a Policy

```python
resource = ten99policy.Policies.modify(
    "po_C9Z2DmfHSF",  # Replace with an existing policy ID
    is_active=False,
)
```

#### Fetching the List of Policies

```python
resource = ten99policy.Policies.list()
```

#### Retrieving a Policy

```python
resource = ten99policy.Policies.retrieve("po_C9Z2DmfHSF")  # Replace with an existing policy ID
```

#### Deleting a Policy

```python
resource = ten99policy.Policies.delete("po_C9Z2DmfHSF")  # Replace with an existing policy ID
```

---

### Quotes

#### Creating a Quote

```python
resource = ten99policy.Quotes.create(
    job="jb_jsb9KEcTpc",
    contractor="cn_yJBbMeq9QA",
    coverage_type=["general", "workers-comp"],
)
```

#### Updating a Quote

```python
resource = ten99policy.Quotes.modify(
    "qt_C9Z2DmfHSF",  # Replace with an existing quote ID
    name="Mechanic",
)
```

#### Fetching the List of Quotes

```python
resource = ten99policy.Quotes.list()
```

#### Retrieving a Quote

```python
resource = ten99policy.Quotes.retrieve("qt_C9Z2DmfHSF")  # Replace with an existing quote ID
```

---

### Assignments

#### Creating an Assignment

```python
resource = ten99policy.Assignments.create(
    contractor="cn_kjLKMtApTv",
    job="jb_D6ZSaoa2MV",
)
```

#### Updating an Assignment

```python
resource = ten99policy.Assignments.modify(
    "as_sF3yUB3BYY",  # Replace with an existing assignment ID
    contractor="cn_kjLKMtApTv",
)
```

#### Fetching the List of Assignments

```python
resource = ten99policy.Assignments.list()
```

#### Retrieving an Assignment

```python
resource = ten99policy.Assignments.retrieve("as_sF3yUB3BYY")  # Replace with an existing assignment ID
```

#### Deleting an Assignment

```python
resource = ten99policy.Assignments.delete("as_xyz")  # Replace with an existing assignment ID
```

---

## Error Handling

The `ten99policy` library raises exceptions for API errors. Use try-except blocks to handle potential errors gracefully.

```python
try:
    resource = ten99policy.Entities.create(
        name="New Entity",
        # ... other parameters
    )
except ten99policy.error.APIError as e:
    print(f"API Error: {e}")
except ten99policy.error.AuthenticationError as e:
    print(f"Authentication Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## Additional Resources

- **1099Policy Website**: [https://www.1099policy.com](https://www.1099policy.com)
- **API Documentation**: [https://www.1099policy.com/docs](https://www.1099policy.com/docs)
- **Developer Guide**: [https://docs.1099policy.com](https://docs.1099policy.com)

## Support

If you encounter any issues or have questions about using the `ten99policy` library, please open an issue on the [GitHub repository](https://github.com/1099policy/1099policy-python) or contact our support team at [support@1099policy.com](mailto:support@1099policy.com).

## License

This library is distributed under the MIT License. See the [LICENSE](https://github.com/1099policy/1099policy-python/blob/main/LICENSE) file in the repository for more information.

---

*Note: Replace placeholder IDs (e.g., `"en_C9Z2DmfHSF"`) with actual IDs from your 1099Policy account when running the code examples.*
