import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating an insurance application session
# -----------------------------------------------------------------------------------*/

resource = ten99policy.InsuranceApplicationSessions.create(
    quote="qt_yVEnbNaWh6",
    success_url="http://example.com/success",
    cancel_url="http://example.com/cancel",
)

# -----------------------------------------------------------------------------------*/
# Updating a session
# -----------------------------------------------------------------------------------*/

resource = ten99policy.InsuranceApplicationSessions.modify(
    "ias_01HZSB299T5D9SCNY98T8P10KC",
    success_url="http://example.com/success",
    cancel_url="http://example.com/cancel",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of insurance application sessions
# -----------------------------------------------------------------------------------*/

resource = ten99policy.InsuranceApplicationSessions.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an insurance application session (replace xxx with an existing insurance application session id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.InsuranceApplicationSessions.retrieve(
    "ias_01HZSB299T5D9SCNY98T8P10KC"
)
