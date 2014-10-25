__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os
import shutil
from io import open

from monty.shutil import copy_r, compress_file, decompress_file, \
    compress_dir, decompress_dir, Command

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')


class CopyRTest(unittest.TestCase):

    def setUp(self):
        os.mkdir(os.path.join(test_dir, "cpr_src"))
        with open(os.path.join(test_dir, "cpr_src", "test"), "w") as f:
            f.write(u"what")
        os.mkdir(os.path.join(test_dir, "cpr_src", "sub"))
        with open(os.path.join(test_dir, "cpr_src", "sub", "testr"), "w") as f:
            f.write(u"what2")

    def test_recursive_copy_and_compress(self):
        copy_r(os.path.join(test_dir, "cpr_src"),
               os.path.join(test_dir, "cpr_dst"))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir, "cpr_dst", "test")))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir, "cpr_dst", "sub", "testr")))

        compress_dir(os.path.join(test_dir, "cpr_src"))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir, "cpr_src", "test.gz")))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir, "cpr_src", "sub",
                                        "testr.gz")))

        decompress_dir(os.path.join(test_dir, "cpr_src"))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir, "cpr_src", "test")))
        self.assertTrue(
            os.path.exists(os.path.join(test_dir, "cpr_src", "sub",
                                        "testr")))
        with open(os.path.join(test_dir, "cpr_src", "test")) as f:
            txt = f.read()
            self.assertEqual(txt, "what")


    def tearDown(self):
        shutil.rmtree(os.path.join(test_dir, "cpr_src"))
        shutil.rmtree(os.path.join(test_dir, "cpr_dst"))


class CompressFileDirTest(unittest.TestCase):

    def setUp(self):
        with open(os.path.join(test_dir, "tempfile"), "w") as f:
            f.write(u"hello world")

    def test_compress_and_decompress_file(self):
        fname = os.path.join(test_dir, "tempfile")
        for fmt in ["gz", "bz2"]:
            compress_file(fname, fmt)
            self.assertTrue(os.path.exists(fname + "." + fmt))
            self.assertFalse(os.path.exists(fname))
            decompress_file(fname + "." + fmt)
            self.assertTrue(os.path.exists(fname))
            self.assertFalse(os.path.exists(fname + "." + fmt))
        with open(fname) as f:
            txt = f.read()
            self.assertEqual(txt, "hello world")
        self.assertRaises(ValueError, compress_file, "whatever", "badformat")

    def tearDown(self):
        os.remove(os.path.join(test_dir, "tempfile"))


class CommandTest(unittest.TestCase):
    def test_command(self):
        """Test Command class"""
        sleep05 = Command("sleep 0.5")

        sleep05.run(timeout=1)
        print(sleep05)
        self.assertEqual(sleep05.retcode, 0)
        self.assertFalse(sleep05.killed)

        sleep05.run(timeout=0.1)
        self.assertNotEqual(sleep05.retcode, 0)
        self.assertTrue(sleep05.killed)


if __name__ == "__main__":
    unittest.main()
