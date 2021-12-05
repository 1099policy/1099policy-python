from t99.api_resources.contractor import Contractor

# -----------------------------------------------------------------------------------*/
# Creating a contractor
#-----------------------------------------------------------------------------------*/

resource = Contractor.create(
    first_name="CEMRE",
    last_name="KARAKULAK",
    email="cemre2@gmail.com",
    phone="51231203",
    address={
        "line1": "IST",
        "locality": "IST",
        "region": "CA",
        "postalcode": 1
    }
)

# -----------------------------------------------------------------------------------*/
# Updating a contractor (replace xxx with an existing contractor id)
#-----------------------------------------------------------------------------------*/

resource = Contractor.modify('cn_tS3wR3UQ5q',
    email='cradexco@gmail.com',
    first_name="x"
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of contractors
#-----------------------------------------------------------------------------------*/

resource = Contractor.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a contractor (replace xxx with an existing contractor id)
#-----------------------------------------------------------------------------------*/

resource = Contractor.retrieve('cn_9TPKz6B9so')

# -----------------------------------------------------------------------------------*/
# Delete a contractor (replace xxx with an existing contractor id)
#-----------------------------------------------------------------------------------*/

resource = Contractor.delete('cn_tS3wR3UQ5q')

print(resource)
