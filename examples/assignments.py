import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating an assignment
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Assignments.create(
    contractor="cn_kjLKMtApTv",
    job="jb_D6ZSaoa2MV",
)

# -----------------------------------------------------------------------------------*/
# Updating an assignment (replace xxx with an existing assignment id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Assignments.modify(
    "an_sF3yUB3BYY",
    contractor="cn_kjLKMtApTv",
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of Assignments
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Assignments.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an assignment (replace xxx with an existing assignment id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Assignments.retrieve("en_BUcNa8jMrq")

# -----------------------------------------------------------------------------------*/
# Delete an assignment (replace xxx with an existing assignment id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Assignments.delete("as_xyz")
