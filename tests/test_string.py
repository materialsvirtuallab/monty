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
import sys

from monty.string import remove_non_ascii, str2unicode, unicode2str


class FuncTest(unittest.TestCase):

    def test_remove_non_ascii(self):
        s = "".join(chr(random.randint(0, 127)) for i in range(10))
        s += "".join(chr(random.randint(128, 150)) for i in range(10))
        clean = remove_non_ascii(s)
        self.assertEqual(len(clean), 10)

    def test_str2unicode(self):
        if sys.version_info.major < 3:
            self.assertEqual(type(str2unicode("a")), unicode)
        else:
            self.assertEqual(type(str2unicode("a")), str)

    def test_unicode2str(self):
        if sys.version_info.major < 3:
            self.assertEqual(type(unicode2str("a")), str)
        else:
            self.assertEqual(type(unicode2str("a")), str)

if __name__ == '__main__':
    unittest.main()
