from __future__ import absolute_import, division, print_function

from ten99policy import error, util, six
from ten99policy.six.moves.urllib.parse import quote_plus


class APIResource():
    @classmethod
    def class_url(cls):
        if cls == APIResource:
            raise NotImplementedError(
                "APIResource is an abstract class.  You should perform "
                "actions on its subclasses (e.g. Jobs, Entities)"
            )

        base = cls.OBJECT_NAME.replace(".", "/")
        return "/api/v1/%s" % (base,)

    def instance_url(self):
        id = self.get("id")

        if not isinstance(id, six.string_types):
            raise error.InvalidRequestError(
                "Could not determine which URL to request: %s instance "
                "has invalid ID: %r, %s. ID should be of type `str` (or"
                " `unicode`)" % (type(self).__name__, id, type(id)),
                "id",
            )

        id = util.utf8(id)
        base = self.class_url()
        extn = quote_plus(id)
        return "%s/%s" % (base, extn)
