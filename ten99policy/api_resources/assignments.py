from ten99policy.api_resources.abstract import CreateableAPIResource
from ten99policy.api_resources.abstract import DeletableAPIResource
from ten99policy.api_resources.abstract import ListableAPIResource
from ten99policy.api_resources.abstract import UpdateableAPIResource


class Assignments(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "assignments"
