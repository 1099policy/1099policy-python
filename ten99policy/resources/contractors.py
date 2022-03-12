from ten99policy.resources.abstract import CreateableAPIResource
from ten99policy.resources.abstract import DeletableAPIResource
from ten99policy.resources.abstract import ListableAPIResource
from ten99policy.resources.abstract import RetrievableAPIResource
from ten99policy.resources.abstract import UpdateableAPIResource


class Contractors(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    RetrievableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "contractors"
