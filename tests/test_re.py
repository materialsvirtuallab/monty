# coding: utf-8
#!/usr/bin/env python

from __future__ import division, unicode_literals

import unittest
import os
from monty.re import regrep

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '6/2/15'


test_dir = os.path.join(os.path.dirname(__file__), 'test_files')


class RegrepTest(unittest.TestCase):

    def test_regrep(self):
        """
        We are making sure a file containing line numbers is read in reverse
        order, i.e. the first line that is read corresponds to the last line.
        number
        """
        fname = os.path.join(test_dir, "three_thousand_lines.txt")
        matches = regrep(fname, {"1": "1(\d+)", "3": "3(\d+)"}, postprocess=int)
        self.assertEqual(len(matches["1"]), 1380)
        self.assertEqual(len(matches["3"]), 571)
        self.assertEqual(matches["1"][0][0][0], 0)

        matches = regrep(fname, {"1": "1(\d+)", "3": "3(\d+)"}, reverse=True,
                         terminate_on_match=True, postprocess=int)
        self.assertEqual(len(matches["1"]), 1)
        self.assertEqual(len(matches["3"]), 11)

if __name__ == "__main__":
    unittest.main()
