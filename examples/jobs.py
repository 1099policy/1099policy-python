import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating a job
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.create(
    name="Truck driver",
    description="Requires a truck",
    duration_hours=20,
    wage=100,
    years_experience=20,
    wage_type="flatfee",
    entity="en_FwZfQRe4aW",
    category_code="jc_MTqpkbkp6G",
)

# -----------------------------------------------------------------------------------*/
# Updating a job (replace xxx with an existing job id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.modify(
    "jb_C9Z2DmfHSF",
    name="Mechanic",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of jobs
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.list()

# -----------------------------------------------------------------------------------*/
# Retrieving a job (replace xxx with an existing job id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.retrieve("jb_C9Z2DmfHSF")

# -----------------------------------------------------------------------------------*/
# Delete a job (replace xxx with an existing job id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Jobs.delete("jb_C9Z2DmfHSF")
