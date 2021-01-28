import unittest
import os
import sys

from collections import namedtuple
from typing import NamedTuple
import pytest  # type: ignore  # Ignore pytest import for mypy

from monty.collections import frozendict, Namespace, AttrDict, \
    FrozenAttrDict, tree
from monty.collections import is_namedtuple
from monty.collections import is_NamedTuple
from monty.collections import validate_NamedTuple

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
    # Testing collections.namedtuple
    a_nt = namedtuple('a', ['x', 'y', 'z'])
    a1 = a_nt(1, 2, 3)
    assert a1 == (1, 2, 3)
    assert is_namedtuple(a1) is True
    assert is_NamedTuple(a1) is False
    with pytest.raises(ValueError, match=r'Cannot validate object of type "a"\.'):
        validate_NamedTuple(a1)
    a_t = tuple([1, 2])
    assert a_t == (1, 2)
    assert is_namedtuple(a_t) is False
    assert is_NamedTuple(a_t) is False
    with pytest.raises(ValueError, match=r'Cannot validate object of type "tuple"\.'):
        validate_NamedTuple(a_t)

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
    assert is_NamedTuple(sublist) is False
    with pytest.raises(ValueError, match=r'Cannot validate object of type "SubList"\.'):
        validate_NamedTuple(sublist)

    # Testing typing.NamedTuple
    A = NamedTuple('A', [('int1', int), ('str1', str)])
    nt = A(3, 'b')
    assert is_NamedTuple(nt) is True
    assert is_namedtuple(nt) is False
    assert validate_NamedTuple(nt) is True
    nt = A(3, 2)
    assert validate_NamedTuple(nt) is False
    nt = A('a', 'b')
    assert validate_NamedTuple(nt) is False

    # Testing typing.NamedTuple with type annotations (for python >= 3.6)
    # This will not work for python < 3.6, leading to a SyntaxError hence the
    # exec here.
    try:
        exec('class B(NamedTuple):\n\
    int1: int = 1\n\
    str1: str = \'a\'\n\
    global B')  # Make the B class available globally
        nt = B(2, 'hello')
        assert is_NamedTuple(nt) is True
        assert is_namedtuple(nt) is False
        assert validate_NamedTuple(nt) is True
        nt = B('a', 'b')
        assert validate_NamedTuple(nt) is False
        nt = B(3, 4)
        assert validate_NamedTuple(nt) is False
    except SyntaxError:
        # Make sure we get this SyntaxError only in the case of python < 3.6.
        assert sys.version_info < (3, 6)


if __name__ == "__main__":
    unittest.main()
