import unittest

from monty.fnmatch import WildCard


class FuncTest(unittest.TestCase):
    def test_match(self):
        wc = WildCard("*.pdf")
        assert wc.match("A.pdf")
        assert not wc.match("A.pdg")


if __name__ == "__main__":
    unittest.main()
