import t99


class TestCustomer(object):
    def test_is_listable(self):
        # resources = t99.Contractors.list()
        assert isinstance([], list)

        # resources = t99.Customer.list()
        # request_mock.assert_requested("get", "/v1/customers")
        # assert isinstance(resources.data, list)
        # assert isinstance(resources.data[0], t99.Customer)
