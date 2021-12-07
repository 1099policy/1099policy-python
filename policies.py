from t99.api_resources.policies import Policies

# -----------------------------------------------------------------------------------*/
# Creating a policy
#-----------------------------------------------------------------------------------*/

resource = Policies.create(
    quote_id="qt_UPmEfS6nNK",
    is_active=True
)

# -----------------------------------------------------------------------------------*/
# Updating a policy (replace xxx with an existing policy id)
#-----------------------------------------------------------------------------------*/

resource = Policies.modify('en_C9Z2DmfHSF',
    is_active=False,
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of policies
#-----------------------------------------------------------------------------------*/

resource = Policies.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a policy (replace xxx with an existing policy id)
#-----------------------------------------------------------------------------------*/

resource = Policies.retrieve('en_C9Z2DmfHSF')

# -----------------------------------------------------------------------------------*/
# Delete a policy (replace xxx with an existing policy id)
#-----------------------------------------------------------------------------------*/

resource = Policies.delete('en_C9Z2DmfHSF')

print(resource)
