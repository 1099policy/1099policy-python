import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Fetching the list of job categories
# -----------------------------------------------------------------------------------*/

resource = ten99policy.JobCategories.list()
