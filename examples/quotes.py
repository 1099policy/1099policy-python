import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating a quote
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Quotes.create(
    job="jb_jsb9KEcTpc",
    contractor="cn_yJBbMeq9QA",
    coverage_type=["general", "workers-comp"],
)

# -----------------------------------------------------------------------------------*/
# Updating a quote (replace xxx with an existing quote id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Quotes.modify(
    "qt_C9Z2DmfHSF",
    name="Mechanic",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of quotes
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Quotes.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a quote (replace xxx with an existing quote id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Quotes.retrieve("qt_C9Z2DmfHSF")
