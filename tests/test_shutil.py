#!/usr/bin/env python

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os
import shutil

from monty.shutil import copy_r


class CopyRTest(unittest.TestCase):

    def setUp(self):
        os.mkdir("cpr_src")
        with open(os.path.join("cpr_src", "test"), "w") as f:
            f.write("what")

    def test_recursive_copy(self):
        copy_r(".", "cpr_dst")
        self.assertTrue(os.path.exists(os.path.join("cpr_dst", "cpr_src",
                                                    "test")))

    def tearDown(self):
        shutil.rmtree("cpr_src")
        shutil.rmtree("cpr_dst")


if __name__ == "__main__":
    unittest.main()
