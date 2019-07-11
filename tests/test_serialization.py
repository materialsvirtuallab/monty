__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import os
import json
try:
    import msgpack
except ImportError:
    msgpack = None

from monty.serialization import dumpfn, loadfn
from monty.tempfile import ScratchDir


class SerialTest(unittest.TestCase):

    def test_dumpfn_loadfn(self):
        d = {"hello": "world"}
        dumpfn(d, "monte_test.json", indent=4)
        d2 = loadfn("monte_test.json")
        self.assertEqual(d, d2)
        os.remove("monte_test.json")
        dumpfn(d, "monte_test.yaml", default_flow_style=False)
        d2 = loadfn("monte_test.yaml")
        self.assertEqual(d, d2)
        dumpfn(d, "monte_test.yaml")
        d2 = loadfn("monte_test.yaml")
        os.remove("monte_test.yaml")

    @unittest.skipIf(msgpack is None, "msgpack-python not installed.")
    def test_mpk(self):
        d = {"hello": "world"}
        dumpfn(d, "monte_test.mpk")
        d2 = loadfn("monte_test.mpk")
        self.assertEqual(d, {k.decode('utf-8'): v.decode('utf-8')
                             for k, v in d2.items()})
        os.remove("monte_test.mpk")

        # Test to ensure basename is respected, and not directory
        with ScratchDir('.'):
            os.mkdir("mpk_test")
            os.chdir("mpk_test")
            fname = os.path.abspath("test_file.json")
            dumpfn({"test": 1}, fname)
            with open("test_file.json", "r") as f:
                reloaded = json.loads(f.read())
            self.assertEqual(reloaded['test'], 1)


if __name__ == "__main__":
    unittest.main()
