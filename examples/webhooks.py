import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating a webhook
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Webhooks.create(
    url="https://webhook.site/1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b",
    description="My First Webhook",
)

# -----------------------------------------------------------------------------------*/
# Updating a webhook (replace xxx with an existing webhook id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Webhooks.modify(
    "whe_H5YMitmVqb6jwNzCMzcAEu",
    url="https://example.com/webhook",
    description="My First Webhook (Updated)",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of entities
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Webhooks.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a webhook (replace xxx with an existing webhook id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Webhooks.retrieve("whe_H5YMitmVqb6jwNzCMzcAEu")

# -----------------------------------------------------------------------------------*/
# Delete a webhook (replace xxx with an existing webhook id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Webhooks.delete("whe_H5YMitmVqb6jwNzCMzcAEu")
