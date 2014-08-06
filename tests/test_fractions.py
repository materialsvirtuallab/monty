__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '8/6/14'

import unittest

from monty.fractions import gcd, lcm


class FuncTestCase(unittest.TestCase):

    def test_gcd(self):
        self.assertEqual(gcd(7, 14, 63), 7)

    def test_lcm(self):
        self.assertEqual(lcm(2, 3, 4), 12)


if __name__ == '__main__':
    unittest.main()
