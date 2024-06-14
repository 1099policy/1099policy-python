from ten99policy.api_resources.abstract import CreateableAPIResource
from ten99policy.api_resources.abstract import ListableAPIResource
from ten99policy.api_resources.abstract import UpdateableAPIResource


class InsuranceApplicationSessions(
    CreateableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "apply/sessions"
