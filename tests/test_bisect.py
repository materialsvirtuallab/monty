import unittest

from monty.bisect import find_ge, find_gt, find_le, find_lt, index


class FuncTestCase(unittest.TestCase):
    def test_funcs(self):
        l = [0, 1, 2, 3, 4]
        assert index(l, 1) == 1
        assert find_lt(l, 1) == 0
        assert find_gt(l, 1) == 2
        assert find_le(l, 1) == 1
        assert find_ge(l, 2) == 2
        # assert index([0, 1, 1.5, 2], 1.501, atol=0.1) == 4


if __name__ == "__main__":
    unittest.main()
