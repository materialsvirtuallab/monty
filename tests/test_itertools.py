# coding: utf-8
# Copyright (c) Materials Virtual Lab.
# Distributed under the terms of the BSD License.

from __future__ import division, unicode_literals, print_function

"""
#TODO: Replace with proper module doc.
"""

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '8/29/14'

import unittest

from monty.itertools import iterator_from_slice


class FuncTest(unittest.TestCase):
    def test_iterator_from_slice(self):

        self.assertEqual(list(iterator_from_slice(slice(0, 6, 2))), [0, 2, 4])

if __name__ == '__main__':
    unittest.main()
