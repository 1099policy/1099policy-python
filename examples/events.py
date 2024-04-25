import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Fetching the list of events
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Events.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an event (replace xxx with an existing event id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Events.retrieve("wh_D1Z2DmgHSF")
