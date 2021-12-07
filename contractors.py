from t99.api_resources.contractors import Contractors

# -----------------------------------------------------------------------------------*/
# Creating a contractor
#-----------------------------------------------------------------------------------*/

resource = Contractors.create(
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

resource = Contractors.modify('cn_tS3wR3UQ5q',
    email='cradexco@gmail.com',
    first_name="x"
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of contractors
#-----------------------------------------------------------------------------------*/

resource = Contractors.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a contractor (replace xxx with an existing contractor id)
#-----------------------------------------------------------------------------------*/

resource = Contractors.retrieve('cn_9TPKz6B9so')

# -----------------------------------------------------------------------------------*/
# Delete a contractor (replace xxx with an existing contractor id)
#-----------------------------------------------------------------------------------*/

resource = Contractors.delete('cn_tS3wR3UQ5q')

print(resource)
