import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Fetching the list of policies for a contractor
# -----------------------------------------------------------------------------------*/

resource = ten99policy.ContractorPolicies.list("cn_ZHrnMCVsaM")
