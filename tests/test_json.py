__version__ = '0.1'

import os
import unittest
import numpy as np
import json
import datetime
import sys
from bson.objectid import ObjectId
from enum import Enum
from collections import namedtuple
from collections import OrderedDict
from typing import NamedTuple

from . import __version__ as tests_version
from monty.json import MSONable, MontyEncoder, MontyDecoder, jsanitize
from monty.json import _load_redirect
from monty.collections import is_namedtuple
from monty.collections import is_NamedTuple

test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")


class GoodMSONClass(MSONable):

    def __init__(self, a, b, c, d=1, **kwargs):
        self.a = a
        self.b = b
        self._c = c
        self._d = d
        self.kwargs = kwargs

    def __eq__(self, other):
        return (self.a == other.a and self.b == other.b and
                self._c == other._c and self._d == other._d and
                self.kwargs == other.kwargs)


class GoodNestedMSONClass(MSONable):

    def __init__(self, a_list, b_dict, c_list_dict_list, **kwargs):
        assert isinstance(a_list, list)
        assert isinstance(b_dict, dict)
        assert isinstance(c_list_dict_list, list)
        assert isinstance(c_list_dict_list[0], dict)
        first_key = list(c_list_dict_list[0].keys())[0]
        assert isinstance(c_list_dict_list[0][first_key], list)
        self.a_list = a_list
        self.b_dict = b_dict
        self._c_list_dict_list = c_list_dict_list
        self.kwargs = kwargs


class EnumTest(MSONable, Enum):
    a = 1
    b = 2


class MSONableTest(unittest.TestCase):

    def setUp(self):
        self.good_cls = GoodMSONClass

        class BadMSONClass(MSONable):

            def __init__(self, a, b):
                self.a = a
                self.b = b

            def as_dict(self):
                d = {"init": {'a': self.a, 'b': self.b}}
                return d

        self.bad_cls = BadMSONClass

        class BadMSONClass2(MSONable):

            def __init__(self, a, b):
                self.a = a
                self.c = b

        self.bad_cls2 = BadMSONClass2

        class AutoMSON(MSONable):

            def __init__(self, a, b):
                self.a = a
                self.b = b

        self.auto_mson = AutoMSON

    def test_to_from_dict(self):
        obj = self.good_cls("Hello", "World", "Python")
        d = obj.as_dict()
        self.assertIsNotNone(d)
        self.good_cls.from_dict(d)
        jsonstr = obj.to_json()
        d = json.loads(jsonstr)
        self.assertTrue(d["@class"], "GoodMSONClass")
        obj = self.bad_cls("Hello", "World")
        d = obj.as_dict()
        self.assertIsNotNone(d)
        self.assertRaises(TypeError, self.bad_cls.from_dict, d)
        obj = self.bad_cls2("Hello", "World")
        self.assertRaises(NotImplementedError, obj.as_dict)
        obj = self.auto_mson(2, 3)
        d = obj.as_dict()
        objd = self.auto_mson.from_dict(d)

    def test_unsafe_hash(self):
        GMC = GoodMSONClass
        a_list = [GMC(1, 1.0, "one"), GMC(2, 2.0, "two")]
        b_dict = {"first": GMC(3, 3.0, "three"), "second": GMC(4, 4.0, "four")}
        c_list_dict_list = [
            {
                "list1": [
                    GMC(5, 5.0, "five"),
                    GMC(6, 6.0, "six"),
                    GMC(7, 7.0, "seven"),
                ],
                "list2": [GMC(8, 8.0, "eight")],
            },
            {
                "list3": [
                    GMC(9, 9.0, "nine"),
                    GMC(10, 10.0, "ten"),
                    GMC(11, 11.0, "eleven"),
                    GMC(12, 12.0, "twelve"),
                ],
                "list4": [GMC(13, 13.0, "thirteen"), GMC(14, 14.0, "fourteen")],
                "list5": [GMC(15, 15.0, "fifteen")],
            },
        ]
        obj = GoodNestedMSONClass(
            a_list=a_list, b_dict=b_dict, c_list_dict_list=c_list_dict_list
        )

        self.assertEqual(
            a_list[0].unsafe_hash().hexdigest(),
            "ea44de0e2ef627be582282c02c48e94de0d58ec6",
        )
        self.assertEqual(
            obj.unsafe_hash().hexdigest(), "44204c8da394e878f7562c9aa2e37c2177f28b81"
        )

    def test_version(self):
        obj = self.good_cls("Hello", "World", "Python")
        d = obj.as_dict()
        self.assertEqual(d["@version"], tests_version)

    def test_nested_to_from_dict(self):
        GMC = GoodMSONClass
        a_list = [GMC(1, 1.0, "one"),
                  GMC(2, 2.0, "two")]
        b_dict = {"first": GMC(3, 3.0, "three"),
                  "second": GMC(4, 4.0, "four")}
        c_list_dict_list = [{"list1": [GMC(5, 5.0, "five"),
                                       GMC(6, 6.0, "six"),
                                       GMC(7, 7.0, "seven")],
                             "list2": [GMC(8, 8.0, "eight")]},
                            {"list3": [GMC(9, 9.0, "nine"),
                                       GMC(10, 10.0, "ten"),
                                       GMC(11, 11.0, "eleven"),
                                       GMC(12, 12.0, "twelve")],
                             "list4": [GMC(13, 13.0, "thirteen"),
                                       GMC(14, 14.0, "fourteen")],
                             "list5": [GMC(15, 15.0, "fifteen")]}]
        obj = GoodNestedMSONClass(a_list=a_list,
                                  b_dict=b_dict,
                                  c_list_dict_list=c_list_dict_list)
        obj_dict = obj.as_dict()
        obj2 = GoodNestedMSONClass.from_dict(obj_dict)
        self.assertTrue([obj2.a_list[ii] == aa for ii, aa in enumerate(obj.a_list)])
        self.assertTrue([obj2.b_dict[kk] == val for kk, val in obj.b_dict.items()])
        self.assertEqual(len(obj.a_list), len(obj2.a_list))
        self.assertEqual(len(obj.b_dict), len(obj2.b_dict))
        s = json.dumps(obj_dict)
        obj3 = json.loads(s, cls=MontyDecoder)
        self.assertTrue([obj2.a_list[ii] == aa for ii, aa in enumerate(obj3.a_list)])
        self.assertTrue([obj2.b_dict[kk] == val for kk, val in obj3.b_dict.items()])
        self.assertEqual(len(obj3.a_list), len(obj2.a_list))
        self.assertEqual(len(obj3.b_dict), len(obj2.b_dict))
        s = json.dumps(obj, cls=MontyEncoder)
        obj4 = json.loads(s, cls=MontyDecoder)
        self.assertTrue([obj4.a_list[ii] == aa for ii, aa in enumerate(obj.a_list)])
        self.assertTrue([obj4.b_dict[kk] == val for kk, val in obj.b_dict.items()])
        self.assertEqual(len(obj.a_list), len(obj4.a_list))
        self.assertEqual(len(obj.b_dict), len(obj4.b_dict))

    def test_enum_serialization(self):
        e = EnumTest.a
        d = e.as_dict()
        e_new = EnumTest.from_dict(d)
        self.assertEqual(e_new.name, e.name)
        self.assertEqual(e_new.value, e.value)

    def test_tuple_serialization(self):
        a = GoodMSONClass(a=1, b=tuple(), c=1)
        afromdict = GoodMSONClass.from_dict(a.as_dict())
        assert type(a.b) is tuple
        assert type(afromdict.b) is tuple
        assert a.b == afromdict.b
        a = GoodMSONClass(a=1, b=[1, tuple([2, tuple([1, 2, 3, 4])])], c=1)
        afromdict = GoodMSONClass.from_dict(a.as_dict())
        assert type(a.b) is list
        assert type(afromdict.b) is list
        assert afromdict.b[0] == 1
        assert type(afromdict.b[1]) is tuple
        assert afromdict.b[1][0] == 2
        assert type(afromdict.b[1][1]) is tuple
        assert afromdict.b[1][1] == (1, 2, 3, 4)

    def test_set_serialization(self):
        a = GoodMSONClass(a={1, 2, 3}, b={'q', 'r'}, c=[14])
        afromdict = GoodMSONClass.from_dict(a.as_dict())
        assert type(afromdict.a) is set

    def test_namedtuple_serialization(self):
        a = namedtuple('A', ['x', 'y', 'zzz'])
        b = GoodMSONClass(a=1, b=a(1, 2, 3), c=1)
        assert is_namedtuple(b.b) is True
        assert b.b._fields == ('x', 'y', 'zzz')
        bfromdict = GoodMSONClass.from_dict(b.as_dict())
        assert is_namedtuple(bfromdict.b) is True
        assert bfromdict.b._fields == ('x', 'y', 'zzz')
        assert bfromdict.b == b.b
        assert bfromdict.b.x == b.b.x
        assert bfromdict.b.y == b.b.y
        assert bfromdict.b.zzz == b.b.zzz

    def test_OrderedDict_serialization(self):
        od = OrderedDict([('val1', 1), ('val2', 2)])
        od['val3'] = '3'
        a = GoodMSONClass(a=1, b=od, c=1)
        assert list(a.b.keys()) == ['val1', 'val2', 'val3']
        afromdict = GoodMSONClass.from_dict(a.as_dict())
        assert type(afromdict.b) is OrderedDict
        assert list(afromdict.b.keys()) == ['val1', 'val2', 'val3']
        assert afromdict.b == a.b

    def test_NamedTuple_serialization(self):
        # "Old style" typing.NamedTuple definition
        A = NamedTuple('MyNamedTuple', [('int1', int), ('str1', str), ('int2', int)])
        A_NT = A(1, 'a', 3)
        a = GoodMSONClass(a=1, b=A_NT, c=1)
        assert is_NamedTuple(a.b)
        afromdict = GoodMSONClass.from_dict(a.as_dict())
        assert is_NamedTuple(afromdict.b)
        assert afromdict.b.__class__.__name__ == 'MyNamedTuple'
        assert afromdict.b._field_types == a.b._field_types
        assert afromdict.b == a.b

        # "New style" typing.NamedTuple definition with class with type annotations (for python >= 3.6)
        # This will not work for python < 3.6, leading to a SyntaxError hence the exec here.
        try:
            exec('class SomeNT(NamedTuple):\n\
            aaa: int\n\
            bbb: float\n\
            ccc: str\n\
            global SomeNT')  # Make the SomeNT class available globally

            myNT = SomeNT(1, 2.1, 'a')

            a = GoodMSONClass(a=1, b=myNT, c=1)
            assert is_NamedTuple(a.b)
            afromdict = GoodMSONClass.from_dict(a.as_dict())
            assert is_NamedTuple(afromdict.b)
            assert afromdict.b.__class__.__name__ == 'SomeNT'
            assert afromdict.b._field_types == a.b._field_types
            assert afromdict.b == a.b
        except SyntaxError:
            # Make sure we get this SyntaxError only in the case of python < 3.6.
            assert sys.version_info < (3, 6)

        try:
            exec('class SomeNT(NamedTuple):\n\
            """My NamedTuple docstring."""\n\
            aaa: int\n\
            bbb: float = 1.0\n\
            ccc: str = \'hello\'\n\
            global SomeNT')  # Make the SomeNT class available globally

            myNT = SomeNT(1, 2.1, 'a')

            a = GoodMSONClass(a=1, b=myNT, c=1)
            assert is_NamedTuple(a.b)
            afromdict = GoodMSONClass.from_dict(a.as_dict())
            assert is_NamedTuple(afromdict.b)
            assert afromdict.b.__class__.__name__ == 'SomeNT'
            assert afromdict.b._field_types == a.b._field_types
            assert afromdict.b == a.b
            assert afromdict.b.__doc__ == a.b.__doc__
        except SyntaxError:
            # Make sure we get this SyntaxError only in the case of python < 3.6.
            assert sys.version_info < (3, 6)

        # Testing "normal classes" types in NamedTuple serialization
        A = NamedTuple('MyNamedTuple', [('int1', int),
                                        ('gmsoncls', GoodMSONClass),
                                        ('gnestedmsoncls', GoodNestedMSONClass)])
        A_NT = A(1,
                 GoodMSONClass(a=1, b=2, c=3),
                 GoodNestedMSONClass(a_list=[3, 4],
                                     b_dict={'a': 2},
                                     c_list_dict_list=[{'ab': ['a', 'b'],
                                                        '34': [3, 4]}]))
        a = GoodMSONClass(a=1, b=A_NT, c=1)
        afromdict = GoodMSONClass.from_dict(a.as_dict())
        assert afromdict.b._field_types == a.b._field_types
        assert a.a == afromdict.a
        assert a.b.gmsoncls == afromdict.b.gmsoncls
        assert a.b.gnestedmsoncls.a_list == afromdict.b.gnestedmsoncls.a_list
        assert a.b.gnestedmsoncls.b_dict == afromdict.b.gnestedmsoncls.b_dict
        assert a.b.gnestedmsoncls._c_list_dict_list == afromdict.b.gnestedmsoncls._c_list_dict_list


class JsonTest(unittest.TestCase):

    def test_as_from_dict(self):
        obj = GoodMSONClass(1, 2, 3, hello="world")
        s = json.dumps(obj, cls=MontyEncoder)
        obj2 = json.loads(s, cls=MontyDecoder)
        self.assertEqual(obj2.a, 1)
        self.assertEqual(obj2.b, 2)
        self.assertEqual(obj2._c, 3)
        self.assertEqual(obj2._d, 1)
        self.assertEqual(obj2.kwargs, {"hello": "world"})
        obj = GoodMSONClass(obj, 2, 3)
        s = json.dumps(obj, cls=MontyEncoder)
        obj2 = json.loads(s, cls=MontyDecoder)
        self.assertEqual(obj2.a.a, 1)
        self.assertEqual(obj2.b, 2)
        self.assertEqual(obj2._c, 3)
        self.assertEqual(obj2._d, 1)
        listobj = [obj, obj2]
        s = json.dumps(listobj, cls=MontyEncoder)
        listobj2 = json.loads(s, cls=MontyDecoder)
        self.assertEqual(listobj2[0].a.a, 1)

    def test_datetime(self):
        dt = datetime.datetime.now()
        jsonstr = json.dumps(dt, cls=MontyEncoder)
        d = json.loads(jsonstr, cls=MontyDecoder)
        self.assertEqual(type(d), datetime.datetime)
        self.assertEqual(dt, d)
        # Test a nested datetime.
        a = {'dt': dt, "a": 1}
        jsonstr = json.dumps(a, cls=MontyEncoder)
        d = json.loads(jsonstr, cls=MontyDecoder)
        self.assertEqual(type(d["dt"]), datetime.datetime)

    def test_numpy(self):
        x = np.array([1, 2, 3], dtype="int64")
        self.assertRaises(TypeError, json.dumps, x)
        djson = json.dumps(x, cls=MontyEncoder)
        d = json.loads(djson)
        self.assertEqual(d["@class"], "array")
        self.assertEqual(d["@module"], "numpy")
        self.assertEqual(d["data"], [1, 2, 3])
        self.assertEqual(d["dtype"], "int64")
        x = json.loads(djson, cls=MontyDecoder)
        self.assertEqual(type(x), np.ndarray)
        x = np.min([1, 2, 3]) > 2
        self.assertRaises(TypeError, json.dumps, x)

    def test_objectid(self):
        oid = ObjectId('562e8301218dcbbc3d7d91ce')
        self.assertRaises(TypeError, json.dumps, oid)
        djson = json.dumps(oid, cls=MontyEncoder)
        x = json.loads(djson, cls=MontyDecoder)
        self.assertEqual(type(x), ObjectId)

    def test_jsanitize(self):
        # clean_json should have no effect on None types.
        d = {"hello": 1, "world": None}
        clean = jsanitize(d)
        self.assertIsNone(clean["world"])
        self.assertEqual(json.loads(json.dumps(d)), json.loads(json.dumps(
            clean)))

        d = {"hello": GoodMSONClass(1, 2, 3)}
        self.assertRaises(TypeError, json.dumps, d)
        clean = jsanitize(d)
        self.assertIsInstance(clean["hello"], str)
        clean_strict = jsanitize(d, strict=True)
        self.assertEqual(clean_strict["hello"]["a"], 1)
        self.assertEqual(clean_strict["hello"]["b"], 2)

        d = {"dt": datetime.datetime.now()}
        clean = jsanitize(d)
        self.assertIsInstance(clean["dt"], str)
        clean = jsanitize(d, allow_bson=True)
        self.assertIsInstance(clean["dt"], datetime.datetime)

        d = {"a": ["b", np.array([1, 2, 3])],
             "b": ObjectId.from_datetime(datetime.datetime.now())}
        clean = jsanitize(d)
        self.assertEqual(clean["a"], ['b', [1, 2, 3]])
        self.assertIsInstance(clean["b"], str)

        rnd_bin = bytes(np.random.rand(10))
        d = {"a": bytes(rnd_bin)}
        clean = jsanitize(d, allow_bson=True)
        self.assertEqual(clean["a"], bytes(rnd_bin))
        self.assertIsInstance(clean["a"], bytes)

    def test_redirect(self):
        MSONable.REDIRECT["tests.test_json"] = {
            "test_class": {"@class": "GoodMSONClass", "@module": "tests.test_json"}
        }

        d = {
            "@class": "test_class",
            "@module": "tests.test_json",
            "a": 1,
            "b": 1,
            "c": 1,
        }

        obj = json.loads(json.dumps(d), cls=MontyDecoder)
        self.assertEqual(type(obj), GoodMSONClass)

        d["@class"] = "not_there"
        obj = json.loads(json.dumps(d), cls=MontyDecoder)
        self.assertEqual(type(obj), dict)

    def test_redirect_settings_file(self):
        data = _load_redirect(os.path.join(test_dir, "test_settings.yaml"))
        self.assertEqual(data, {'old_module': {'old_class': {'@class': 'new_class', '@module': 'new_module'}}})

    def test_complex_enc_dec(self):
        a = tuple([0, 2, 4])
        a_jsonstr = json.dumps(a, cls=MontyEncoder)
        a_from_jsonstr = json.loads(a_jsonstr, cls=MontyDecoder)
        assert type(a_from_jsonstr) is tuple

        nt = namedtuple('A', ['x', 'y', 'zzz'])
        nt2 = namedtuple('ABC', ['ab', 'cd', 'ef'])
        od = OrderedDict([('val1', 1), ('val2', GoodMSONClass(a=a, b=nt2(1, 2, 3), c=1))])
        od['val3'] = '3'

        NT = NamedTuple('MyTypingNamedTuple', [('A1', int), ('A2', float), ('B1', str)])
        a_NT = NT(2, 3.1, 'hello')
        a_NT_jsonstr = json.dumps(a_NT, cls=MontyEncoder)
        a_NT_from_jsonstr = json.loads(a_NT_jsonstr, cls=MontyDecoder)
        assert is_NamedTuple(a_NT_from_jsonstr) is True

        try:
            exec('class NT_def(NamedTuple):\n\
            """My NamedTuple with defaults."""\n\
            aaa: int\n\
            bbb: float = 1.0\n\
            ccc: str = \'hello\'\n\
            global NT_def')  # Make the NT_def class available globally

            myNT = NT_def(1, 2.1)
            myNT_jsonstr = json.dumps(myNT, cls=MontyEncoder)
            myNT_from_jsonstr = json.loads(myNT_jsonstr, cls=MontyDecoder)
            assert is_NamedTuple(myNT_from_jsonstr)
            assert myNT_from_jsonstr.__doc__ == 'My NamedTuple with defaults.'
            assert myNT_from_jsonstr.ccc == 'hello'
        except SyntaxError:
            # Make sure we get this SyntaxError only in the case of python < 3.6.
            assert sys.version_info < (3, 6)

        obj = nt(x=a, y=od, zzz=[1, 2, 3])
        obj_jsonstr = json.dumps(obj, cls=MontyEncoder)
        obj_from_jsonstr = json.loads(obj_jsonstr, cls=MontyDecoder)

        assert is_namedtuple(obj_from_jsonstr) is True
        assert obj_from_jsonstr.__class__.__name__ == 'A'
        assert type(obj_from_jsonstr.x) is tuple
        assert obj_from_jsonstr.x == (0, 2, 4)
        assert type(obj_from_jsonstr.y) is OrderedDict
        assert list(obj_from_jsonstr.y.keys()) == ['val1', 'val2', 'val3']
        assert obj_from_jsonstr.y['val1'] == 1
        assert type(obj_from_jsonstr.y['val2']) is GoodMSONClass
        assert type(obj_from_jsonstr.y['val2'].a) is tuple
        assert obj_from_jsonstr.y['val2'].a == (0, 2, 4)
        assert is_namedtuple(obj_from_jsonstr.y['val2'].b) is True
        assert obj_from_jsonstr.y['val2'].b.__class__.__name__ == 'ABC'
        assert obj_from_jsonstr.y['val2'].b.ab == 1
        assert obj_from_jsonstr.y['val2'].b.cd == 2
        assert obj_from_jsonstr.y['val2'].b.ef == 3
        assert obj_from_jsonstr.y['val3'] == '3'

    def test_set_json(self):
        myset = {1, 2, 3}
        myset_jsonstr = json.dumps(myset, cls=MontyEncoder)
        myset_from_jsonstr = json.loads(myset_jsonstr, cls=MontyDecoder)
        assert type(myset_from_jsonstr) is set
        assert myset_from_jsonstr == myset



if __name__ == "__main__":
    unittest.main()
