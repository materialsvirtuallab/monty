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

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')


class CopyRTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        os.mkdir("src")
        with open(os.path.join("src", "test"), "w") as f:
            f.write("what")

    def test_recursive_copy(self):
        copy_r(".", "dst")
        self.assertTrue(os.path.exists(os.path.join("dst", "src", "test")))
        self.assertTrue(os.path.exists(os.path.join("dst", "__init__.py")))

    def tearDown(self):
        shutil.rmtree("src")
        shutil.rmtree("dst")
        os.chdir(self.cwd)



if __name__ == "__main__":
    unittest.main()
