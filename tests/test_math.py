# coding: utf-8
#!/usr/bin/env python

from __future__ import division, unicode_literals

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest

from monty.math import nCr, nPr


class FuncTest(unittest.TestCase):

    def test_nCr(self):
        self.assertEqual(nCr(4, 2), 6)

    def test_deprecated_property(self):
        self.assertEqual(nPr(4, 2), 12)


if __name__ == "__main__":
    unittest.main()
