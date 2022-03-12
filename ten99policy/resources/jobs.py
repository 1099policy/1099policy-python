from ten99policy.resources.abstract import CreateableAPIResource
from ten99policy.resources.abstract import DeletableAPIResource
from ten99policy.resources.abstract import ListableAPIResource
from ten99policy.resources.abstract import UpdateableAPIResource


class Jobs(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "jobs"
