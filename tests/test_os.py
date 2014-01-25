#!/usr/bin/env python

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os

from monty.os.path import which


class PathTest(unittest.TestCase):

    def test_which(self):
        py = which("python")
        self.assertEqual(os.path.basename(py), "python")


if __name__ == "__main__":
    unittest.main()
