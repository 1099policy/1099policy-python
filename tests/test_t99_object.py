from __future__ import absolute_import, division, print_function

import datetime
import json
import pickle
from copy import copy, deepcopy

import pytest

import t99
from t99 import six


SAMPLE_INVOICE = json.loads(
    """
{
  "amount_due": 1305,
  "attempt_count": 0,
  "attempted": true,
  "charge": "ch_wajkQ5aDTzFs5v",
  "closed": true,
  "customer": "cus_osllUe2f1BzrRT",
  "date": 1338238728,
  "discount": null,
  "ending_balance": 0,
  "id": "in_t9mHb2hpK7mml1",
  "livemode": false,
  "next_payment_attempt": null,
  "object": "invoice",
  "paid": true,
  "period_end": 1338238728,
  "period_start": 1338238716,
  "starting_balance": -8695,
  "subtotal": 10000,
  "total": 10000,
  "lines": {
    "invoiceitems": [],
    "prorations": [],
    "subscriptions": [
      {
        "plan": {
          "interval": "month",
          "object": "plan",
          "identifier": "expensive",
          "currency": "usd",
          "livemode": false,
          "amount": 10000,
          "name": "Expensive Plan",
          "trial_period_days": null,
          "id": "expensive"
        },
        "period": {
          "end": 1340917128,
          "start": 1338238728
        },
        "amount": 10000
      }
    ]
  }
}
"""
)


class TestT99Object(object):
    def test_initializes_with_parameters(self):
        obj = t99.t99_object.T99Object(
            "foo", "bar", myparam=5, yourparam="boo"
        )

        assert obj.id == "foo"
        assert obj.api_key == "bar"

    def test_access(self):
        obj = t99.t99_object.T99Object("myid", "mykey", myparam=5)

        # Empty
        with pytest.raises(AttributeError):
            obj.myattr
        with pytest.raises(KeyError):
            obj["myattr"]
        assert obj.get("myattr", "def") == "def"
        assert obj.get("myattr") is None

        # Setters
        obj.myattr = "myval"
        obj["myitem"] = "itval"
        assert obj.setdefault("mydef", "sdef") == "sdef"

        # Getters
        assert obj.setdefault("myattr", "sdef") == "myval"
        assert obj.myattr == "myval"
        assert obj["myattr"] == "myval"
        assert obj.get("myattr") == "myval"

        assert sorted(obj.keys()) == ["id", "myattr", "mydef", "myitem"]

        assert sorted(obj.values()) == ["itval", "myid", "myval", "sdef"]

        # Illegal operations
        with pytest.raises(ValueError):
            obj.foo = ""

    def test_refresh_from(self, mocker):
        obj = t99.t99_object.T99Object.construct_from(
            {"foo": "bar", "trans": "me"}, "mykey"
        )

        assert obj.api_key == "mykey"
        assert obj.foo == "bar"
        assert obj["trans"] == "me"
        assert obj.t99_version is None
        assert obj.t99_account is None
        assert obj.last_response is None

        last_response = mocker.Mock()
        obj.refresh_from(
            {"foo": "baz", "johnny": 5},
            "key2",
            t99_version="2017-08-15",
            t99_account="acct_foo",
            last_response=last_response,
        )

        assert obj.johnny == 5
        assert obj.foo == "baz"
        with pytest.raises(AttributeError):
            obj.trans
        assert obj.api_key == "key2"
        assert obj.t99_version == "2017-08-15"
        assert obj.t99_account == "acct_foo"
        assert obj.last_response == last_response

        obj.refresh_from(
            {"trans": 4, "metadata": {"amount": 42}}, "key2", True
        )

        assert obj.foo == "baz"
        assert obj.trans == 4

    def test_passing_nested_refresh(self):
        obj = t99.t99_object.T99Object.construct_from(
            {"foos": {"type": "list", "data": [{"id": "nested"}]}},
            "key",
            t99_account="acct_foo",
        )

        nested = obj.foos.data[0]

        assert obj.api_key == "key"
        assert nested.id == "nested"
        assert nested.api_key == "key"
        assert nested.t99_account == "acct_foo"

    def test_refresh_from_nested_object(self):
        obj = t99.t99_object.T99Object.construct_from(
            SAMPLE_INVOICE, "key"
        )

        assert len(obj.lines.subscriptions) == 1
        assert isinstance(
            obj.lines.subscriptions[0], t99.t99_object.T99Object
        )
        assert obj.lines.subscriptions[0].plan.interval == "month"

    def test_to_json(self):
        obj = t99.t99_object.T99Object.construct_from(
            SAMPLE_INVOICE, "key"
        )

        self.check_invoice_data(json.loads(str(obj)))

    def check_invoice_data(self, data):
        # Check rough structure
        assert len(list(data.keys())) == 20
        assert len(list(data["lines"].keys())) == 3
        assert len(data["lines"]["invoiceitems"]) == 0
        assert len(data["lines"]["subscriptions"]) == 1

        # Check various data types
        assert data["date"] == 1338238728
        assert data["next_payment_attempt"] is None
        assert data["livemode"] is False
        assert data["lines"]["subscriptions"][0]["plan"]["interval"] == "month"

    def test_repr(self):
        obj = t99.t99_object.T99Object("foo", "bar", myparam=5)

        obj["object"] = u"\u4e00boo\u1f00"
        obj.date = datetime.datetime.fromtimestamp(1511136000)

        res = repr(obj)

        if six.PY2:
            res = six.text_type(repr(obj), "utf-8")

        assert u"<T99Object \u4e00boo\u1f00" in res
        assert u"id=foo" in res
        assert u'"date": 1511136000' in res

    def test_pickling(self):
        obj = t99.t99_object.T99Object("foo", "bar", myparam=5)

        obj["object"] = "boo"
        obj.refresh_from(
            {
                "fala": "lalala",
                # ensures that empty strings are correctly unpickled in Py3
                "emptystring": "",
            },
            api_key="bar",
            partial=True,
        )

        assert obj.fala == "lalala"

        pickled = pickle.dumps(obj)
        newobj = pickle.loads(pickled)

        assert newobj.id == "foo"
        assert newobj.api_key == "bar"
        assert newobj["object"] == "boo"
        assert newobj.fala == "lalala"
        assert newobj.emptystring == ""

    def test_deletion(self):
        obj = t99.t99_object.T99Object("id", "key")

        obj.coupon = "foo"
        assert obj.coupon == "foo"

        del obj.coupon
        with pytest.raises(AttributeError):
            obj.coupon

        obj.refresh_from({"coupon": "foo"}, api_key="bar", partial=True)
        assert obj.coupon == "foo"

    def test_deletion_metadata(self):
        obj = t99.t99_object.T99Object.construct_from(
            {"metadata": {"key": "value"}}, "mykey"
        )

        assert obj.metadata["key"] == "value"

        del obj.metadata["key"]
        with pytest.raises(KeyError):
            obj.metadata["key"]

    def test_copy(self):
        nested = t99.t99_object.T99Object.construct_from(
            {"value": "bar"}, "mykey"
        )
        obj = t99.t99_object.T99Object.construct_from(
            {"empty": "", "value": "foo", "nested": nested},
            "mykey",
            t99_account="myaccount",
        )

        copied = copy(obj)

        assert copied.empty == ""
        assert copied.value == "foo"
        assert copied.nested.value == "bar"

        assert copied.api_key == "mykey"
        assert copied.t99_account == "myaccount"

        # Verify that we're not deep copying nested values.
        assert id(nested) == id(copied.nested)

    def test_deepcopy(self):
        nested = t99.t99_object.T99Object.construct_from(
            {"value": "bar"}, "mykey"
        )
        obj = t99.t99_object.T99Object.construct_from(
            {"empty": "", "value": "foo", "nested": nested},
            "mykey",
            t99_account="myaccount",
        )

        copied = deepcopy(obj)

        assert copied.empty == ""
        assert copied.value == "foo"
        assert copied.nested.value == "bar"

        assert copied.api_key == "mykey"
        assert copied.t99_account == "myaccount"

        # Verify that we're actually deep copying nested values.
        assert id(nested) != id(copied.nested)

    def test_to_dict_recursive(self):
        foo = t99.t99_object.T99Object.construct_from(
            {"value": "foo"}, "mykey"
        )
        bar = t99.t99_object.T99Object.construct_from(
            {"value": "bar"}, "mykey"
        )
        obj = t99.t99_object.T99Object.construct_from(
            {"empty": "", "value": "foobar", "nested": [foo, bar]}, "mykey"
        )

        d = obj.to_dict_recursive()
        assert d == {
            "empty": "",
            "value": "foobar",
            "nested": [{"value": "foo"}, {"value": "bar"}],
        }
        assert not isinstance(
            d["nested"][0], t99.t99_object.T99Object
        )
        assert not isinstance(
            d["nested"][1], t99.t99_object.T99Object
        )

    def test_serialize_empty_string_unsets(self):
        class SerializeToEmptyString(t99.t99_object.T99Object):
            def serialize(self, previous):
                return ""

        nested = SerializeToEmptyString.construct_from(
            {"value": "bar"}, "mykey"
        )
        obj = t99.t99_object.T99Object.construct_from(
            {"nested": nested}, "mykey"
        )

        assert obj.serialize(None) == {"nested": ""}
