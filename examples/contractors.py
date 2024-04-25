import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating a contractor
# -----------------------------------------------------------------------------------*/

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

# -----------------------------------------------------------------------------------*/
# Updating a contractor (replace xxx with an existing contractor id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Contractors.modify(
    "cn_tS3wR3UQ5q",
    email="john.doe@gmail.com",
    first_name="George",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of contractors
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Contractors.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a contractor (replace xxx with an existing contractor id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Contractors.retrieve("cn_9TPKz6B9so")

# -----------------------------------------------------------------------------------*/
# Delete a contractor (replace xxx with an existing contractor id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Contractors.delete("cn_tS3wR3UQ5q")
