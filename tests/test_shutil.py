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

from monty.shutil import copy_r, compress_file, compress_dir

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')

# class CopyRTest(unittest.TestCase):
#
#     def setUp(self):
#         os.mkdir(os.path.join(test_dir, "cpr_src"))
#         with open(os.path.join(test_dir, "cpr_src", "test"), "w") as f:
#             f.write("what")
#
#     def test_recursive_copy(self):
#         copy_r(os.path.join(test_dir, "cpr_src"),
#                os.path.join(test_dir, "cpr_dst"))
    #     self.assertTrue(
    #         os.path.exists(os.path.join(test_dir, "cpr_dst", "test")))
    #
    # def tearDown(self):
    #     shutil.rmtree(os.path.join(test_dir, "cpr_src"))
    #     shutil.rmtree(os.path.join(test_dir, "cpr_dst"))


class CompressFileDirTest(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(test_dir, "tempfile"), "w") as f:
            f.write("hello world")

    def test_compress_file(self):
        compress_file(os.path.join(test_dir, "tempfile"))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir,
                                        "tempfile.gz")))

    def tearDown(self):
        os.remove(os.path.join(test_dir, "tempfile.gz"))

if __name__ == "__main__":
    unittest.main()
