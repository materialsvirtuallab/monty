from __future__ import annotations

import pytest

from monty.collections import (
    AttrDict,
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


def test_CaseInsensitiveDictUpper():
    upper_dict = CaseInsensitiveDictUpper({"HI": "world"})
    assert "hi" in upper_dict
    assert upper_dict["HI"] == "world"
    assert upper_dict["hi"] == "world"

    # Test setter and getter
    upper_dict["a"] = 1
    assert upper_dict["a"] == 1
    assert upper_dict["A"] == 1

    upper_dict["B"] = 2  # upper case
    assert upper_dict["b"] == 2
    assert upper_dict["B"] == 2

    # Test update with setter
    upper_dict["B"] = 3
    assert upper_dict["b"] == 3
    assert upper_dict["B"] == 3

    upper_dict["b"] = 4
    assert upper_dict["b"] == 4
    assert upper_dict["B"] == 4

    # Test update with `update`
    upper_dict.update({"c": 5, "D": 6})
    assert upper_dict["C"] == 5
    assert upper_dict["c"] == 5
    assert upper_dict["D"] == 6
    assert upper_dict["d"] == 6

    # Test update with `|=`
    upper_dict |= {"e": 7, "F": 8}
    assert upper_dict["E"] == 7
    assert upper_dict["e"] == 7
    assert upper_dict["F"] == 8
    assert upper_dict["f"] == 8

    # Test `setdefault`
    assert upper_dict.setdefault("g", 9) == 9  # Add new key
    assert upper_dict["G"] == 9
    assert upper_dict["g"] == 9
    assert upper_dict.setdefault("g", 10) == 9  # Existing key remains unchanged
    assert upper_dict["G"] == 9

    # Test membership check with `in`
    assert "g" in upper_dict
    assert "G" in upper_dict
    assert "non-existent" not in upper_dict

    # Test `__delitem__`
    del upper_dict["hi"]
    assert "hi" not in upper_dict
    assert "HI" not in upper_dict

    # Test `del dct[key]`
    del upper_dict["b"]
    assert "b" not in upper_dict
    assert "B" not in upper_dict

    # Test `pop(key)`
    popped_value = upper_dict.pop("c")
    assert popped_value == 5
    assert "c" not in upper_dict
    assert "C" not in upper_dict

    # Test `pop(key)` with default value (key exists)
    popped_value = upper_dict.pop("d", "default")
    assert popped_value == 6
    assert "d" not in upper_dict
    assert "D" not in upper_dict

    # Test `pop(key)` with default value (key doesn't exist)
    popped_value = upper_dict.pop("non-existent", "default")
    assert popped_value == "default"
    assert "non-existent" not in upper_dict


class TestTree:
    def test_tree(self):
        x = tree()
        x["a"]["b"]["c"]["d"] = 1
        assert "b" in x["a"]
        assert "c" not in x["a"]
        assert "c" in x["a"]["b"]
        assert x["a"]["b"]["c"]["d"] == 1
