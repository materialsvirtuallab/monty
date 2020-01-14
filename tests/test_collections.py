import unittest
import os

from collections import namedtuple

from monty.collections import frozendict, Namespace, AttrDict, \
    FrozenAttrDict, tree
from monty.collections import is_namedtuple

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')


class FrozenDictTest(unittest.TestCase):

    def test_frozen_dict(self):
        d = frozendict({"hello": "world"})
        self.assertRaises(KeyError, d.__setitem__, "k", "v")
        self.assertRaises(KeyError, d.update, {"k": "v"})
        self.assertEqual(d["hello"], "world")

    def test_namespace_dict(self):
        d = Namespace(foo="bar")
        d["hello"] = "world"
        self.assertEqual(d["foo"], "bar")
        self.assertRaises(KeyError, d.__setitem__, "foo", "spam")

    def test_attr_dict(self):
        d = AttrDict(foo=1, bar=2)
        self.assertEqual(d.bar, 2)
        self.assertEqual(d["foo"], d.foo)
        d.bar = "hello"
        self.assertEqual(d["bar"], "hello")

    def test_frozen_attrdict(self):
        d = FrozenAttrDict({"hello": "world", 1: 2})
        self.assertEqual(d["hello"], "world")
        self.assertEqual(d.hello, "world")
        self.assertRaises(KeyError, d.update, {"updating": 2})
        with self.assertRaises(KeyError):  d["foo"] = "bar"
        with self.assertRaises(KeyError):  d.foo = "bar"
        with self.assertRaises(KeyError): d.hello = "new"


class TreeTest(unittest.TestCase):

    def test_tree(self):
        x = tree()
        x['a']['b']['c']['d'] = 1
        self.assertIn('b', x['a'])
        self.assertNotIn('c', x['a'])
        self.assertIn('c', x['a']['b'])
        self.assertEqual(x['a']['b']['c']['d'], 1)


def test_is_namedtuple():
    a_nt = namedtuple('a', ['x', 'y', 'z'])
    a1 = a_nt(1, 2, 3)
    assert a1 == (1, 2, 3)
    assert is_namedtuple(a1) is True
    a_t = tuple([1, 2])
    assert a_t == (1, 2)
    assert is_namedtuple(a_t) is False

    class SubList(list):
        def _fields(self):
            return []
        def _fields_defaults(self):
            return []
        def _asdict(self):
            return {}

    sublist = SubList([3, 2, 1])
    assert sublist == [3, 2, 1]
    assert is_namedtuple(sublist) is False


if __name__ == "__main__":
    unittest.main()
