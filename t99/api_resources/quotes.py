from t99.api_resources.abstract import CreateableAPIResource
from t99.api_resources.abstract import ListableAPIResource
from t99.api_resources.abstract import UpdateableAPIResource


class Quotes(
    CreateableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "quotes"
