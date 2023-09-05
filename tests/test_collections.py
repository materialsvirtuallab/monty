import os
import unittest

from monty.collections import AttrDict, FrozenAttrDict, Namespace, frozendict, tree

test_dir = os.path.join(os.path.dirname(__file__), "test_files")


class FrozenDictTest(unittest.TestCase):
    def test_frozen_dict(self):
        d = frozendict({"hello": "world"})
        self.assertRaises(KeyError, d.__setitem__, "k", "v")
        self.assertRaises(KeyError, d.update, {"k": "v"})
        assert d["hello"] == "world"

    def test_namespace_dict(self):
        d = Namespace(foo="bar")
        d["hello"] = "world"
        assert d["foo"] == "bar"
        self.assertRaises(KeyError, d.__setitem__, "foo", "spam")

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
        self.assertRaises(KeyError, d.update, {"updating": 2})
        with self.assertRaises(KeyError):
            d["foo"] = "bar"
        with self.assertRaises(KeyError):
            d.foo = "bar"
        with self.assertRaises(KeyError):
            d.hello = "new"


class TreeTest(unittest.TestCase):
    def test_tree(self):
        x = tree()
        x["a"]["b"]["c"]["d"] = 1
        assert "b" in x["a"]
        assert "c" not in x["a"]
        assert "c" in x["a"]["b"]
        assert x["a"]["b"]["c"]["d"] == 1


if __name__ == "__main__":
    unittest.main()
