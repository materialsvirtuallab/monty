from __future__ import annotations

from collections import UserDict

import pytest

from monty.collections import (
    AttrDict,
    ControlledDict,
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


class TestControlledDict:
    def test_add_allowed(self):
        dct = ControlledDict(a=1)
        dct.allow_add = True

        dct["b"] = 2
        assert dct["b"] == 2

        dct.update(d=3)
        assert dct["d"] == 3

        dct.setdefault("e", 4)
        assert dct["e"] == 4

    def test_add_disabled(self):
        dct = ControlledDict(a=1)
        dct.allow_add = False

        with pytest.raises(TypeError, match="add is disabled"):
            dct["b"] = 2

        with pytest.raises(TypeError, match="add is disabled"):
            dct.update(b=2)

        with pytest.raises(TypeError, match="add is disabled"):
            dct.setdefault("c", 2)

    def test_update_allowed(self):
        dct = ControlledDict(a=1)
        dct.allow_update = True

        dct["a"] = 2
        assert dct["a"] == 2

        dct.update({"a": 3})
        assert dct["a"] == 3

        dct.setdefault("a", 4)  # existing key
        assert dct["a"] == 3

    def test_update_disabled(self):
        dct = ControlledDict(a=1)
        dct.allow_update = False

        with pytest.raises(TypeError, match="update is disabled"):
            dct["a"] = 2

        with pytest.raises(TypeError, match="update is disabled"):
            dct.update({"a": 3})

        with pytest.raises(TypeError, match="update is disabled"):
            dct.setdefault("a", 4)

    def test_del_allowed(self):
        dct = ControlledDict(a=1, b=2, c=3, d=4)
        dct.allow_del = True

        del dct["a"]
        assert "a" not in dct

        val = dct.pop("b")
        assert val == 2 and "b" not in dct

        val = dct.popitem()
        assert val == ("c", 3) and "c" not in dct

        dct.clear()
        assert dct == {}

    def test_del_disabled(self):
        dct = ControlledDict(a=1)
        dct.allow_del = False

        with pytest.raises(TypeError, match="delete is disabled"):
            del dct["a"]

        with pytest.raises(TypeError, match="delete is disabled"):
            dct.pop("a")

        with pytest.raises(TypeError, match="delete is disabled"):
            dct.popitem()

        with pytest.raises(TypeError, match="delete is disabled"):
            dct.clear()

    def test_frozen_like(self):
        """Make sure add and update are allowed at init time."""
        ControlledDict.allow_add = False
        ControlledDict.allow_update = False

        dct = ControlledDict({"hello": "world"})
        assert isinstance(dct, UserDict)
        assert dct["hello"] == "world"

        assert not dct.allow_add
        assert not dct.allow_update


def test_frozendict():
    dct = frozendict({"hello": "world"})
    assert isinstance(dct, UserDict)
    assert dct["hello"] == "world"

    assert not dct.allow_add
    assert not dct.allow_update
    assert not dct.allow_del

    # Test setter
    with pytest.raises(TypeError, match="add is disabled"):
        dct["key"] = "val"

    # Test update
    with pytest.raises(TypeError, match="add is disabled"):
        dct.update(key="val")

    # Test pop
    with pytest.raises(TypeError, match="delete is disabled"):
        dct.pop("key")

    # Test delete
    with pytest.raises(TypeError, match="delete is disabled"):
        del dct["key"]


def test_namespace_dict():
    dct = Namespace(key="val")
    assert isinstance(dct, UserDict)

    # Test setter
    dct["hello"] = "world"
    assert dct["key"] == "val"

    # Test update (not allowed)
    with pytest.raises(TypeError, match="update is disabled"):
        dct["key"] = "val"

    with pytest.raises(TypeError, match="update is disabled"):
        dct.update({"key": "val"})

    # Test delete (not allowed)
    with pytest.raises(TypeError, match="delete is disabled"):
        del dct["key"]


def test_attr_dict():
    dct = AttrDict(foo=1, bar=2)

    # Test get attribute
    assert dct.bar == 2
    assert dct["foo"] is dct.foo

    # Test key not found error
    with pytest.raises(KeyError, match="no-such-key"):
        dct["no-such-key"]

    # Test setter
    dct.bar = "hello"
    assert dct["bar"] == "hello"

    # Test delete
    del dct.bar
    assert "bar" not in dct

    # Test builtin dict method shadowing
    with pytest.warns(UserWarning, match="shadows dict method"):
        dct["update"] = "value"


def test_frozen_attrdict():
    dct = FrozenAttrDict({"hello": "world", 1: 2})
    assert isinstance(dct, dict)

    # Test get value
    assert dct["hello"] == "world"
    assert dct.hello == "world"
    assert dct["hello"] is dct.hello

    # Test adding item
    with pytest.raises(
        TypeError, match="FrozenAttrDict does not support item assignment"
    ):
        dct["foo"] = "bar"
    with pytest.raises(
        TypeError, match="FrozenAttrDict does not support item assignment"
    ):
        dct.foo = "bar"

    # Test modifying existing item
    with pytest.raises(
        TypeError, match="FrozenAttrDict does not support item assignment"
    ):
        dct.hello = "new"
    with pytest.raises(
        TypeError, match="FrozenAttrDict does not support item assignment"
    ):
        dct["hello"] = "new"

    # Test update
    with pytest.raises(TypeError, match="FrozenAttrDict does not support update"):
        dct.update({"hello": "world"})

    # Test pop
    with pytest.raises(TypeError, match="FrozenAttrDict does not support pop"):
        dct.pop("hello")

    with pytest.raises(TypeError, match="FrozenAttrDict does not support popitem"):
        dct.popitem()

    # Test delete
    with pytest.raises(TypeError, match="FrozenAttrDict does not support deletion"):
        del dct["hello"]

    with pytest.raises(TypeError, match="FrozenAttrDict does not support deletion"):
        del dct.hello

    with pytest.raises(TypeError, match="FrozenAttrDict does not support clear"):
        dct.clear()


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
