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

from monty.json import MSONable, MSONError, MontyEncoder, MontyDecoder, \
    jsanitize


class GoodMSONClass(MSONable):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def as_dict(self):
        d = {'a': self.a, 'b': self.b}
        return d

    @classmethod
    def from_dict(cls, d):
        return GoodMSONClass(d['a'], d['b'])


class MSONableTest(unittest.TestCase):

    def setUp(self):
        self.good_cls = GoodMSONClass

        class BadMSONClass(MSONable):

            def __init__(self, a, b):
                self.a = a
                self.b = b

            def as_dict(self):
                d = {'a': self.a, 'b': self.b}
                return d

        self.bad_cls = BadMSONClass

    def test_to_from_dict(self):
        obj = self.good_cls("Hello", "World")
        d = obj.as_dict()
        self.assertIsNotNone(d)
        self.good_cls.from_dict(d)
        obj = self.bad_cls("Hello", "World")
        d = obj.as_dict()
        self.assertIsNotNone(d)
        self.assertRaises(MSONError, self.bad_cls.from_dict, d)


class JsonTest(unittest.TestCase):

    def test_datetime(self):
        dt = datetime.datetime.now()
        jsonstr = json.dumps(dt, cls=MontyEncoder)
        d = json.loads(jsonstr, cls=MontyDecoder)
        self.assertEqual(type(d), datetime.datetime)
        self.assertEqual(dt, d)
        #Test a nested datetime.
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

    def test_jsanitize(self):
        #clean_json should have no effect on None types.
        d = {"hello": 1, "world": None}
        clean = jsanitize(d)
        self.assertIsNone(clean["world"])
        self.assertEqual(json.loads(json.dumps(d)), json.loads(json.dumps(
            clean)))

        d = {"hello": GoodMSONClass(1, 2)}
        self.assertRaises(TypeError, json.dumps, d)
        clean = jsanitize(d)
        self.assertIsInstance(clean["hello"], six.string_types)
        clean_strict = jsanitize(d, strict=True)
        self.assertEqual(clean_strict["hello"]["a"], 1)
        self.assertEqual(clean_strict["hello"]["b"], 2)

if __name__ == "__main__":
    unittest.main()
