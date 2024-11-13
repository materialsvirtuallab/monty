from __future__ import annotations

import pytest

from monty.collections import (
    AttrDict,
    FrozenAttrDict,
    MongoDict,
    Namespace,
    dict2namedtuple,
    frozendict,
    tree,
)


def test_tree():
    x = tree()
    x["a"]["b"]["c"]["d"] = 1
    assert "b" in x["a"]
    assert "c" not in x["a"]
    assert "c" in x["a"]["b"]
    assert x["a"]["b"]["c"]["d"] == 1


def test_frozendict():
    dct = frozendict({"hello": "world"})
    assert dct["hello"] == "world"

    with pytest.raises(KeyError, match="Cannot overwrite existing key"):
        dct["key"] == "val"

    with pytest.raises(KeyError, match="Cannot overwrite existing key"):
        dct.update(key="value")


def test_namespace_dict():
    dct = Namespace(key="val")
    dct["hello"] = "world"
    assert dct["key"] == "val"

    with pytest.raises(KeyError, match="Cannot overwrite existing key"):
        dct["key"] = "val"
    with pytest.raises(KeyError, match="Cannot overwrite existing key"):
        dct.update({"key": "val"})
    with pytest.raises(KeyError, match="Cannot overwrite existing key"):
        dct |= {"key": "val"}


def test_attr_dict():
    dct = AttrDict(foo=1, bar=2)
    assert dct.bar == 2
    assert dct["foo"] is dct.foo

    # Test accessing values
    dct.bar = "hello"
    assert dct["bar"] == "hello"


def test_frozen_attrdict():
    dct = FrozenAttrDict({"hello": "world", 1: 2})
    assert dct["hello"] == "world"
    assert dct.hello == "world"

    # Test adding item
    with pytest.raises(KeyError, match="You cannot modify attribute"):
        dct["foo"] = "bar"
    with pytest.raises(KeyError, match="You cannot modify attribute"):
        dct.foo = "bar"

    # Test modifying existing item
    with pytest.raises(KeyError, match="You cannot modify attribute"):
        dct.hello = "new"
    with pytest.raises(KeyError, match="You cannot modify attribute"):
        dct["hello"] = "new"


def test_mongo_dict():
    m_dct = MongoDict({"a": {"b": 1}, "x": 2})
    assert m_dct.a.b == 1
    assert m_dct.x == 2
    assert "a" in m_dct
    assert "b" in m_dct.a
    assert m_dct["a"] == {"b": 1}


def test_dict2namedtuple():
    # Init from dict
    tpl = dict2namedtuple(foo=1, bar="hello")
    assert isinstance(tpl, tuple)
    assert tpl.foo == 1 and tpl.bar == "hello"

    # Init from list of tuples
    tpl = dict2namedtuple([("foo", 1), ("bar", "hello")])
    assert isinstance(tpl, tuple)
    assert tpl[0] == 1
    assert tpl[1] == "hello"
    assert tpl[0] is tpl.foo and tpl[1] is tpl.bar
