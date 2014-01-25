#!/usr/bin/env python

"""
TODO: Modify module doc.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "1/24/14"


import unittest
import os

test_dir = os.path.join(os.path.dirname(__file__), "..", "..", 'test_files')

from monty.json import loadf, dumpf


class JsonTest(unittest.TestCase):

    def test_dumpf(self):
        d = {"hello": "world"}
        dumpf(d, "monte_test.json", indent=4)
        d2 = loadf("monte_test.json")
        self.assertEqual(d, d2)
        os.remove("monte_test.json")


if __name__ == "__main__":
    unittest.main()
