import t99

# -----------------------------------------------------------------------------------*/
# Creating an entity
#-----------------------------------------------------------------------------------*/

resource = t99.Entities.create(
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
# Updating an entity (replace xxx with an existing entity id)
#-----------------------------------------------------------------------------------*/

resource = t99.Entities.modify('en_C9Z2DmfHSF',
    name='California Roll',
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of entities
#-----------------------------------------------------------------------------------*/

resource = t99.Entities.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an entity (replace xxx with an existing entity id)
#-----------------------------------------------------------------------------------*/

resource = t99.Entities.retrieve('en_BUcNa8jMrq')

# -----------------------------------------------------------------------------------*/
# Delete an entity (replace xxx with an existing entity id)
#-----------------------------------------------------------------------------------*/

resource = t99.Entities.delete('en_C9Z2DmfHSF')
