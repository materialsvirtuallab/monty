from __future__ import annotations

import pytest

from monty.collections import (
    AttrDict,
    CaseInsensitiveDictLower,
    CaseInsensitiveDictUpper,
    FrozenAttrDict,
    Namespace,
    frozendict,
    tree,
)


class TestFrozenDict:
    def test_frozen_dict(self):
        d = frozendict({"hello": "world"})
        with pytest.raises(KeyError):
            d["k"] == "v"
        assert d["hello"] == "world"

    def test_namespace_dict(self):
        d = Namespace(foo="bar")
        d["hello"] = "world"
        assert d["foo"] == "bar"
        with pytest.raises(KeyError):
            d.update({"foo": "spam"})

    def test_attr_dict(self):
        d = AttrDict(foo=1, bar=2)
        assert d.bar == 2
        assert d["foo"] == d.foo
        d.bar = "hello"
        assert d["bar"] == "hello"

    def test_frozen_attrdict(self):
        d = FrozenAttrDict({"hello": "world", 1: 2})
        assert d["hello"] == "world"
        assert d.hello == "world"
        with pytest.raises(KeyError):
            d["updating"] == 2

        with pytest.raises(KeyError):
            d["foo"] = "bar"
        with pytest.raises(KeyError):
            d.foo = "bar"
        with pytest.raises(KeyError):
            d.hello = "new"


class TestCaseInsensitiveDictUpper:
    def setup_method(self):
        self.upper_dict = CaseInsensitiveDictUpper({"HI": "world"})

    def test_init(self):
        # Test init from Mapping
        dct = CaseInsensitiveDictUpper({"key1": "value1", "Key2": "value2"})
        assert dct["key1"] == "value1"
        assert dct["KEY1"] == "value1"
        assert dct["Key2"] == "value2"
        assert dct["key2"] == "value2"

        # Test init from Iterable
        dct = CaseInsensitiveDictUpper([("key1", "value1"), ("Key2", "value2")])
        assert dct["key1"] == "value1"
        assert dct["KEY1"] == "value1"
        assert dct["Key2"] == "value2"
        assert dct["key2"] == "value2"

        # Test init with kwargs
        dct = CaseInsensitiveDictUpper(key1="value1", Key2="value2")
        assert dct["key1"] == "value1"
        assert dct["KEY1"] == "value1"
        assert dct["Key2"] == "value2"
        assert dct["key2"] == "value2"

    def test_converter(self):
        str_key = "upper"
        assert CaseInsensitiveDictUpper._converter(str_key) == "UPPER"

        # Test non-string object handling (should be returned as is)
        int_key = 1
        assert CaseInsensitiveDictUpper._converter(int_key) == 1

        tup_key = (1, 2, 3)
        assert CaseInsensitiveDictUpper._converter(tup_key) == (1, 2, 3)

    def test_membership(self):
        assert "hi" in self.upper_dict
        assert "HI" in self.upper_dict
        assert self.upper_dict["HI"] == "world"
        assert self.upper_dict["hi"] == "world"

    def test_setter_and_getter(self):
        self.upper_dict["a"] = 1
        assert self.upper_dict["a"] == 1
        assert self.upper_dict["A"] == 1

        self.upper_dict["B"] = 2
        assert self.upper_dict["b"] == 2
        assert self.upper_dict["B"] == 2
        assert self.upper_dict.get("b") == 2
        assert self.upper_dict.get("B") == 2

    def test_update(self):
        # Test with Mapping
        self.upper_dict.update({"c": 5, "D": 6})
        assert self.upper_dict["C"] == 5
        assert self.upper_dict["c"] == 5
        assert self.upper_dict["D"] == 6
        assert self.upper_dict["d"] == 6

        # Test with Iterable
        self.upper_dict.update([("e", 7), ("F", 8)])
        assert self.upper_dict["E"] == 7
        assert self.upper_dict["e"] == 7
        assert self.upper_dict["F"] == 8
        assert self.upper_dict["f"] == 8

        # Test with kwargs
        self.upper_dict.update(g=9, H=10)
        assert self.upper_dict["G"] == 9
        assert self.upper_dict["g"] == 9
        assert self.upper_dict["H"] == 10
        assert self.upper_dict["h"] == 10

        # Test combined
        self.upper_dict.update({"I": 11}, j=12, k=13)
        assert self.upper_dict["I"] == 11
        assert self.upper_dict["i"] == 11
        assert self.upper_dict["J"] == 12
        assert self.upper_dict["j"] == 12
        assert self.upper_dict["K"] == 13
        assert self.upper_dict["k"] == 13

    def test_ior_operator(self):
        self.upper_dict |= {"e": 7, "F": 8}
        assert self.upper_dict["E"] == 7
        assert self.upper_dict["e"] == 7
        assert self.upper_dict["F"] == 8
        assert self.upper_dict["f"] == 8

    def test_or_operator(self):
        # Test with another CaseInsensitiveDictUpper
        other = CaseInsensitiveDictUpper({"E": 7, "F": 8})
        result = self.upper_dict | other
        assert isinstance(result, CaseInsensitiveDictUpper)
        assert result["E"] == 7
        assert result["e"] == 7
        assert result["F"] == 8
        assert result["f"] == 8
        assert result["HI"] == "world"
        assert result["hi"] == "world"

        # Test with a regular dict
        other = {"g": 9, "H": 10}
        result = self.upper_dict | other
        assert isinstance(result, CaseInsensitiveDictUpper)
        assert result["G"] == 9
        assert result["g"] == 9
        assert result["H"] == 10
        assert result["h"] == 10
        assert result["HI"] == "world"
        assert result["hi"] == "world"

    def test_setdefault(self):
        assert self.upper_dict.setdefault("g", 9) == 9
        assert self.upper_dict["G"] == 9
        assert self.upper_dict.setdefault("g", 10) == 9  # Unchanged
        assert self.upper_dict["G"] == 9

    def test_delete_items(self):
        # Test `__delitem__`
        del self.upper_dict["hi"]
        assert "hi" not in self.upper_dict
        assert "HI" not in self.upper_dict

        # Test `del dct[key]`
        self.upper_dict["b"] = 4
        del self.upper_dict["b"]
        assert "b" not in self.upper_dict
        assert "B" not in self.upper_dict

    def test_pop(self):
        # Test `pop(key)`
        self.upper_dict["c"] = 5
        popped_value = self.upper_dict.pop("c")
        assert popped_value == 5
        assert "c" not in self.upper_dict
        assert "C" not in self.upper_dict

        # Test `pop(key)` with default value
        popped_value = self.upper_dict.pop("non-existent", "default")
        assert popped_value == "default"
        assert "non-existent" not in self.upper_dict


class TestCaseInsensitiveDictLower:
    """Most case-insensitive dict behaviour would be tested in
    `TestCaseInsensitiveDictUpper` to avoid duplicate.
    """

    def test_converter(self):
        str_key = "Capitalized"
        assert CaseInsensitiveDictLower._converter(str_key) == "capitalized"

        # Test non-string object handling (should be returned as is)
        int_key = 1
        assert CaseInsensitiveDictLower._converter(int_key) == 1

        tup_key = (1, 2, 3)
        assert CaseInsensitiveDictLower._converter(tup_key) == (1, 2, 3)


class TestTree:
    def test_tree(self):
        x = tree()
        x["a"]["b"]["c"]["d"] = 1
        assert "b" in x["a"]
        assert "c" not in x["a"]
        assert "c" in x["a"]["b"]
        assert x["a"]["b"]["c"]["d"] == 1
