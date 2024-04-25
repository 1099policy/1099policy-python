import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating an entity
# -----------------------------------------------------------------------------------*/

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

# -----------------------------------------------------------------------------------*/
# Updating an entity (replace xxx with an existing entity id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Entities.modify(
    "en_C9Z2DmfHSF",
    name="California Roll",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of entities
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Entities.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an entity (replace xxx with an existing entity id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Entities.retrieve("en_BUcNa8jMrq")

# -----------------------------------------------------------------------------------*/
# Delete an entity (replace xxx with an existing entity id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Entities.delete("en_C9Z2DmfHSF")
