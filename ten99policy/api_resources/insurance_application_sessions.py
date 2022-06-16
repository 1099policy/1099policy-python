from ten99policy.api_resources.abstract import CreateableAPIResource
from ten99policy.api_resources.abstract import ListableAPIResource


class InsuranceApplicationSessions(
    CreateableAPIResource,
    ListableAPIResource,
):
    OBJECT_NAME = "apply/sessions"
