#!/usr/bin/env python

"""
TODO: Modify unittest doc.
"""

from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "2/28/14"

import unittest
import random

from monty.string import remove_non_ascii


class FuncTest(unittest.TestCase):

    def test_remove_non_ascii(self):
        s = "".join(chr(random.randint(0, 127)) for i in xrange(10))
        s += "".join(chr(random.randint(128, 150)) for i in xrange(10))
        clean = remove_non_ascii(s)
        self.assertEqual(len(clean), 10)


if __name__ == '__main__':
    unittest.main()
