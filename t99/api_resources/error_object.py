from __future__ import absolute_import, division, print_function

from t99.t99_object import T99Object


class ErrorObject(T99Object):
    def refresh_from(
        self,
        values,
        api_key=None,
        partial=False,
        t99_version=None,
        t99_account=None,
        last_response=None,
    ):
        return super(ErrorObject, self).refresh_from(
            values,
            api_key,
            partial,
            t99_version,
            t99_account,
            last_response,
        )
