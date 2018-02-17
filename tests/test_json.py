__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import numpy as np
import json
import datetime
import six
from bson.objectid import ObjectId
from ast import literal_eval


from monty.json import MSONable, MontyEncoder, MontyDecoder, jsanitize


class GoodMSONClass(MSONable):

    def __init__(self, a, b, c, d=1, **kwargs):
        self.a = a
        self.b = b
        self._c = c
        self._d = d
        self.kwargs = kwargs


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
        self.assertIsInstance(clean["hello"], six.string_types)
        clean_strict = jsanitize(d, strict=True)
        self.assertEqual(clean_strict["hello"]["a"], 1)
        self.assertEqual(clean_strict["hello"]["b"], 2)

        d = {"dt": datetime.datetime.now()}
        clean = jsanitize(d)
        self.assertIsInstance(clean["dt"], six.string_types)
        clean = jsanitize(d, allow_bson=True)
        self.assertIsInstance(clean["dt"], datetime.datetime)

        d = {"a": ["b", np.array([1, 2, 3])],
             "b": ObjectId.from_datetime(datetime.datetime.now())}
        clean = jsanitize(d)
        self.assertEqual(clean["a"], ['b', [1, 2, 3]])
        self.assertIsInstance(clean["b"], six.string_types)

        rnd_bin = six.binary_type(np.random.rand(10))
        d = {"a": six.binary_type(rnd_bin)}
        clean = jsanitize(d, allow_bson=True)
        self.assertEqual(clean["a"], six.binary_type(rnd_bin))
        self.assertIsInstance(clean["a"], six.binary_type)

if __name__ == "__main__":
    unittest.main()
