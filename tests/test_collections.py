__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os

from monty.collections import frozendict

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

class FrozenDictTest(unittest.TestCase):

    def test_frozen_dict(self):
        d = frozendict({"hello": "world"})
        self.assertRaises(KeyError, d.__setitem__, "k", "v")
        self.assertEqual(d["hello"], "world")

if __name__ == "__main__":
    unittest.main()
