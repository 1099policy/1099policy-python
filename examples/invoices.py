import ten99policy

# You can configure the environment for 1099Policy API (sandbox|production)
# ten99policy.environment = 'sandbox'

# -----------------------------------------------------------------------------------*/
# Creating an invoice
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Invoices.create(
    contractor="cn_ti8eXviE4A",
    job="jb_rajdrwMUKi",
    gross_pay=1000,
    paycycle_startdate=1730476766,
    paycycle_enddate=1730476766,
)

# # -----------------------------------------------------------------------------------*/
# Updating an invoice (replace xxx with an existing invoice id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Invoices.modify(
    "in_m47rNFQ3PS",
    gross_pay=1500,
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of invoices
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Invoices.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an invoice (replace xxx with an existing invoice id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Invoices.retrieve("in_tcbma8oShU")

# -----------------------------------------------------------------------------------*/
# Delete an invoice (replace xxx with an existing invoice id)
# -----------------------------------------------------------------------------------*/

resource = ten99policy.Invoices.delete("in_tcbma8oShU")
