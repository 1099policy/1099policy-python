import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Fetching the list of entities
# -----------------------------------------------------------------------------------*/

resource = ten99policy.JobCategories.list()
