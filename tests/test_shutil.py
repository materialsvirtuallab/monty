__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os
import shutil
import tempfile
from gzip import GzipFile
from io import open

from monty.shutil import copy_r, compress_file, decompress_file, \
    compress_dir, decompress_dir, gzip_dir, remove

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

class GzipDirTest(unittest.TestCase):

    def setUp(self):
        os.mkdir(os.path.join(test_dir, "gzip_dir"))
        with open(os.path.join(test_dir, "gzip_dir", "tempfile"), "w") as f:
            f.write(u"what")

        self.mtime = os.path.getmtime(os.path.join(test_dir, "gzip_dir",
                                                   "tempfile"))

    def test_gzip(self):
        full_f = os.path.join(test_dir, "gzip_dir", "tempfile")
        gzip_dir(os.path.join(test_dir, "gzip_dir"))

        self.assertTrue(os.path.exists("{}.gz".format(full_f)))
        self.assertFalse((os.path.exists(full_f)))

        with GzipFile("{}.gz".format(full_f)) as g:
            self.assertEquals(g.readline().decode("utf-8"), "what")

        self.assertAlmostEqual(os.path.getmtime("{}.gz".format(full_f)),
                               self.mtime, 4)

    def tearDown(self):
        shutil.rmtree(os.path.join(test_dir, "gzip_dir"))

class RemoveTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.mkdtemp(dir=test_dir)
        self.tempfile = tempfile.mkstemp(dir=self.tempdir)[1]

        os.symlink(self.tempdir, os.path.join(test_dir, "temp_link"))
        self.templink = os.path.join(test_dir, "temp_link")

    def tearDown(self):
        if os.path.isfile(self.tempfile):
            os.remove(self.tempfile)

        if os.path.islink(self.templink):
            os.unlink(self.templink)

        if os.path.isdir(self.tempdir):
            shutil.rmtree(self.tempdir)

    def test_remove_file(self):
        print(os.listdir(test_dir))
        remove(self.tempfile)
        self.assertFalse(os.path.isfile(self.tempfile))

    def test_remove_folder(self):
        remove(self.tempdir)
        self.assertFalse(os.path.isfile(self.tempfile))
        self.assertFalse(os.path.isdir(self.tempdir))

    def test_remove_symlink(self):
        remove(self.templink)
        self.assertTrue(os.path.isfile(self.tempfile))
        self.assertTrue(os.path.isdir(self.tempdir))
        self.assertFalse(os.path.islink(self.templink))

    def test_remove_symlink_follow(self):
        print(self.tempfile)
        remove(self.templink, follow_symlink=True)
        self.assertFalse(os.path.isfile(self.tempfile))
        self.assertFalse(os.path.isdir(self.tempdir))
        self.assertFalse(os.path.islink(self.templink))

if __name__ == "__main__":
    unittest.main()
