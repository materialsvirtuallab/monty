__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os

from monty.serialization import dumpfn, loadfn
from yaml import Dumper

class SerialTest(unittest.TestCase):

    def test_dumpf_loadf(self):
        d = {"hello": "world"}
        dumpfn(d, "monte_test.json", indent=4)
        d2 = loadfn("monte_test.json")
        self.assertEqual(d, d2)
        os.remove("monte_test.json")
        dumpfn(d, "monte_test.yaml", default_flow_style=False)
        d2 = loadfn("monte_test.yaml")
        self.assertEqual(d, d2)
        dumpfn(d, "monte_test.yaml", Dumper=Dumper)
        d2 = loadfn("monte_test.yaml")
        os.remove("monte_test.yaml")


if __name__ == "__main__":
    unittest.main()
