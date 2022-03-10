import t99policy


class TestCustomer(object):
    def test_is_listable(self):
        resources = t99policy.Contractors.list()
        print(resources)
        assert isinstance([], list)

        # resources = t99policy.Customer.list()
        # request_mock.assert_requested("get", "/v1/customers")
        # assert isinstance(resources.data, list)
        # assert isinstance(resources.data[0], t99policy.Customer)
