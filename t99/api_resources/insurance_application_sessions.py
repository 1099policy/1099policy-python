from t99.api_resources.abstract import CreateableAPIResource
from t99.api_resources.abstract import ListableAPIResource


class InsuranceApplicationSessions(
    CreateableAPIResource,
    ListableAPIResource,
):
    OBJECT_NAME = "apply/sessions"
