from __future__ import absolute_import, division, print_function

from ten99policy.ten99policy_object import TEN99POLICYObject


class ErrorObject(TEN99POLICYObject):
    def refresh_from(
        self,
        values,
        api_key=None,
        partial=False,
        last_response=None,
    ):
        return super(ErrorObject, self).refresh_from(
            values,
            api_key,
            partial,
            last_response,
        )
