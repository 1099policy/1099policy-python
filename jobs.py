from t99.api_resources.jobs import Jobs

# -----------------------------------------------------------------------------------*/
# Creating a job
#-----------------------------------------------------------------------------------*/

resource = Jobs.create(
    name="Truck driver",
    description="Requires a truck",
    duration_hours=20,
    wage=100,
    years_experience=20,
    wage_type="flatfee",
    entity_id="en_FwZfQRe4aW",
    category_code="jc_MTqpkbkp6G"
)

# -----------------------------------------------------------------------------------*/
# Updating a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = Jobs.modify('en_C9Z2DmfHSF',
    name='Mechanic',
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of jobs
#-----------------------------------------------------------------------------------*/

resource = Jobs.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = Jobs.retrieve('en_C9Z2DmfHSF')

# -----------------------------------------------------------------------------------*/
# Delete a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = Jobs.delete('en_C9Z2DmfHSF')

print(resource)
