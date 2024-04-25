import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating a policy
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Policies.create(
    quote_id="qt_UPmEfS6nNK",
    is_active=True,
)

# -----------------------------------------------------------------------------------*/
# Updating a policy (replace xxx with an existing policy id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Policies.modify(
    "en_C9Z2DmfHSF",
    is_active=False,
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of policies
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Policies.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a policy (replace xxx with an existing policy id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Policies.retrieve("en_C9Z2DmfHSF")

# -----------------------------------------------------------------------------------*/
# Delete a policy (replace xxx with an existing policy id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Policies.delete("en_C9Z2DmfHSF")
