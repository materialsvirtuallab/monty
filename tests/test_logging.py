__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest

from six.moves import StringIO

import logging
import time
from monty.logging import logged

@logged()
def add(a, b):
    return a + b


class FuncTest(unittest.TestCase):
    def test_logged(self):
        s = StringIO()
        logging.basicConfig(level=logging.DEBUG, stream=s)
        add(1, 2)

if __name__ == "__main__":
    unittest.main()
