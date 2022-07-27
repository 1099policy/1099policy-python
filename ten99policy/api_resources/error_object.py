from __future__ import absolute_import, division, print_function

from ten99policy.ten99policy_object import Ten99PolicyObject


class ErrorObject(Ten99PolicyObject):
    def refresh_from(
        self,
        values,
        api_key=None,
        partial=False,
        ten99policy_version=None,
        ten99policy_environment=None,
        last_response=None,
    ):
        return super(ErrorObject, self).refresh_from(
            values,
            api_key,
            partial,
            ten99policy_version,
            ten99policy_environment,
            last_response,
        )
