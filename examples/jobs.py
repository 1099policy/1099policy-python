import t99

# -----------------------------------------------------------------------------------*/
# Creating a job
#-----------------------------------------------------------------------------------*/

resource = t99.Jobs.create(
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

resource = t99.Jobs.modify('en_C9Z2DmfHSF',
    name='Mechanic',
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of jobs
#-----------------------------------------------------------------------------------*/

resource = t99.Jobs.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = t99.Jobs.retrieve('en_C9Z2DmfHSF')

# -----------------------------------------------------------------------------------*/
# Delete a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = t99.Jobs.delete('en_C9Z2DmfHSF')

print(resource)
