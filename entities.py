from t99.api_resources.entities import Entities

# -----------------------------------------------------------------------------------*/
# Creating a entity
#-----------------------------------------------------------------------------------*/

resource = Entities.create(
    name="Brooklyn Bowl",
    coverage_limit={
        "aggregate_limit": "200000000",
        "occurrence_limit": "100000000"
    },
    address={
        "line1": "3639 18th St",
        "line2": "",
        "locality": "San Francisco",
        "region": "CA",
        "postalcode": "94110"
    },
    required_coverage=["general", "workers-comp"]
)

# -----------------------------------------------------------------------------------*/
# Updating a entity (replace xxx with an existing entity id)
#-----------------------------------------------------------------------------------*/

resource = Entities.modify('en_C9Z2DmfHSF',
    name='California Roll',
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of entities
#-----------------------------------------------------------------------------------*/

resource = Entities.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a entity (replace xxx with an existing entity id)
#-----------------------------------------------------------------------------------*/

resource = Entities.retrieve('en_BUcNa8jMrq')

# -----------------------------------------------------------------------------------*/
# Delete a entity (replace xxx with an existing entity id)
#-----------------------------------------------------------------------------------*/

resource = Entities.delete('en_C9Z2DmfHSF')

print(resource)
