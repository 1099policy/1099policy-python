from ten99policy.api_resources.abstract import ListableAPIResource


class ContractorPolicies(
    ListableAPIResource,
):
    OBJECT_NAME = "contractors/{}/policies"
