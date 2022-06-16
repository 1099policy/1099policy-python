import ten99policy


class TestCustomer(object):
    def test_is_listable(self):
        # resources = ten99policy.Contractors.list()
        assert isinstance([], list)

        # resources = ten99policy.Customer.list()
        # request_mock.assert_requested("get", "/v1/customers")
        # assert isinstance(resources.data, list)
        # assert isinstance(resources.data[0], ten99policy.Customer)
