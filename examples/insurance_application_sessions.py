import t99

# -----------------------------------------------------------------------------------*/
# Creating an insurance application session
#-----------------------------------------------------------------------------------*/

resource = t99.InsuranceApplicationSessions.create(
    quote="qt_yVEnbNaWh6",
    success_url="http://example.com/success",
    cancel_url="http://example.com/cancel"
)

# -----------------------------------------------------------------------------------*/
# Fetching the list of insurance application sessions
#-----------------------------------------------------------------------------------*/

resource = t99.InsuranceApplicationSessions.list()

# -----------------------------------------------------------------------------------*/
# Retrieving an insurance application session (replace xxx with an existing insurance application session id)
#-----------------------------------------------------------------------------------*/

resource = t99.InsuranceApplicationSessions.retrieve('ias_01G4ZVGEXG4DQHZ1TZ6ANAWPD8')