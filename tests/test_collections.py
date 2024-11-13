from __future__ import annotations

import os
from collections import namedtuple

import pytest

from monty.collections import (
    AttrDict,
    FrozenAttrDict,
    Namespace,
    dict2namedtuple,
    frozendict,
    tree,
)

TEST_DIR = os.path.join(os.path.dirname(__file__), "test_files")


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
    """TODO: add test"""


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
