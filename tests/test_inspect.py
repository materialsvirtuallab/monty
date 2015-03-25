# coding: utf-8
from __future__ import division, unicode_literals

import unittest
import os

from monty.inspect import *


class InspectTest(unittest.TestCase):

    def test_find_caller(self):
        """Testing find_caller..."""
        caller = find_caller()
        assert caller.name == "test_find_caller"
        assert os.path.basename(caller.filename) == "test_inspect.py"


if __name__ == "__main__":
    unittest.main()
