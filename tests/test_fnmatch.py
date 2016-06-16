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

from monty.fnmatch import WildCard


class FuncTest(unittest.TestCase):

    def test_match(self):
        wc = WildCard("*.pdf")
        self.assertTrue(wc.match("A.pdf"))
        self.assertFalse(wc.match("A.pdg"))

if __name__ == '__main__':
    unittest.main()
