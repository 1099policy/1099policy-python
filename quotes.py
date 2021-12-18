from t99.api_resources.quotes import Quotes

# -----------------------------------------------------------------------------------*/
# Creating a quote
#-----------------------------------------------------------------------------------*/

resource = Quotes.create(
    job_id="jb_jsb9KEcTpc",
    contractor_id="cn_yJBbMeq9QA",
    coverage_type="general"
)

# -----------------------------------------------------------------------------------*/
# Updating a quote (replace xxx with an existing quote id)
#-----------------------------------------------------------------------------------*/

resource = Quotes.modify('en_C9Z2DmfHSF',
    name='Mechanic',
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of quotes
#-----------------------------------------------------------------------------------*/

resource = Quotes.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a quote (replace xxx with an existing quote id)
#-----------------------------------------------------------------------------------*/

resource = Quotes.retrieve('en_C9Z2DmfHSF')

print(resource)
