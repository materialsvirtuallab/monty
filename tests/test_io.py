__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os
from io import open

from monty.io import reverse_readline, zopen

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


class ZopenTest(unittest.TestCase):

    def test_zopen(self):
        with zopen(os.path.join(test_dir, "myfile.gz"), mode="rt") as f:
            self.assertEqual(f.read(), "HelloWorld.\n\n")
        with zopen(os.path.join(test_dir, "myfile.bz2"), mode="rt") as f:
            self.assertEqual(f.read(), "HelloWorld.\n\n")
        with zopen(os.path.join(test_dir, "myfile.bz2"), "rt") as f:
            self.assertEqual(f.read(), "HelloWorld.\n\n")
        with zopen(os.path.join(test_dir, "myfile"), mode="rt") as f:
            self.assertEqual(f.read(), "HelloWorld.\n\n")

if __name__ == "__main__":
    unittest.main()
