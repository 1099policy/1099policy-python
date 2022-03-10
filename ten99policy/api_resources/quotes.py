from ten99policy.api_resources.abstract import CreateableAPIResource
from ten99policy.api_resources.abstract import ListableAPIResource
from ten99policy.api_resources.abstract import UpdateableAPIResource


class Quotes(
    CreateableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "quotes"
