import ten99policy

# -----------------------------------------------------------------------------------*/
# Creating a job
#-----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.create(
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

resource = ten99policy.Jobs.modify('en_C9Z2DmfHSF',
    name='Mechanic',
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of jobs
#-----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.retrieve('en_C9Z2DmfHSF')

# -----------------------------------------------------------------------------------*/
# Delete a job (replace xxx with an existing job id)
#-----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.delete('en_C9Z2DmfHSF')

print(resource)
