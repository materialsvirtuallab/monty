# coding: utf-8
from __future__ import division, unicode_literals

import unittest
import os

from monty.inspect import *

class LittleCatA(object):
    pass

class LittleCatB(LittleCatA):
    pass

class LittleCatC(object):
    pass

class LittleCatD(LittleCatB):
    pass


class InspectTest(unittest.TestCase):

    def test_find_caller(self):
        """Testing find_caller..."""
        caller = find_caller()
        assert caller.name == "test_find_caller"
        assert os.path.basename(caller.filename) == "test_inspect.py"

    def test_find_top_pyfile(self):
        # Not a real test. Need something better.
        self.assertTrue(find_top_pyfile())

    def test_all_subclasses(self):
        self.assertEqual(all_subclasses(LittleCatA), [LittleCatB, LittleCatD])

if __name__ == "__main__":
    unittest.main()
