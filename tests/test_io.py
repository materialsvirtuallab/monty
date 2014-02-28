#!/usr/bin/env python

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import shutil
import os

from monty.io import reverse_readline, ScratchDir

test_dir = os.path.join(os.path.dirname(__file__), 'test_files')


class ReverseReadlineTest(unittest.TestCase):
    NUMLINES = 3000

    def test_reverse_readline(self):
        """
        We are making sure a file containing line numbers is read in reverse
        order, i.e. the first line that is read corresponds to the last line.
        number
        """
        with open(os.path.join(test_dir, "three_thousand_lines.txt")) as f:
            for idx, line in enumerate(reverse_readline(f)):
                self.assertEqual(int(line), self.NUMLINES - idx,
                                 "read_backwards read {} whereas it should "
                                 "have read {}".format(
                                     int(line), self.NUMLINES - idx))

    def test_empty_file(self):
        """
        make sure an empty file does not throw an error when reverse_readline
        is called this was a problem with an earlier implementation
        """
        with open(os.path.join(test_dir, "empty_file.txt")) as f:
            for idx, line in enumerate(reverse_readline(f)):
                raise ValueError("an empty file is being read!")


class ScratchDirTest(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        os.chdir(test_dir)
        self.scratch_root = os.path.join(test_dir, "..", "..", "tempscratch")
        os.mkdir(self.scratch_root)

    def test_with_copy(self):

        with ScratchDir(self.scratch_root, copy_from_current_on_enter=True,
                        copy_to_current_on_exit=True) as d:
            with open("scratch_text", "w") as f:
                f.write("write")
            files = os.listdir(d)
            self.assertIn("scratch_text", files)
            self.assertIn("empty_file.txt", files)

        #Make sure the tempdir is deleted.
        self.assertFalse(os.path.exists(d))
        files = os.listdir(".")
        self.assertIn("scratch_text", files)
        os.remove("scratch_text")

    def test_no_copy(self):

        with ScratchDir(self.scratch_root, copy_from_current_on_enter=False,
                        copy_to_current_on_exit=False) as d:
            with open("scratch_text", "w") as f:
                f.write("write")
            files = os.listdir(d)
            self.assertIn("scratch_text", files)
            self.assertNotIn("empty_file.txt", files)

        #Make sure the tempdir is deleted.
        self.assertFalse(os.path.exists(d))
        files = os.listdir(".")
        self.assertNotIn("scratch_text", files)

    def tearDown(self):
        os.chdir(self.cwd)
        shutil.rmtree(self.scratch_root)


if __name__ == "__main__":
    unittest.main()
