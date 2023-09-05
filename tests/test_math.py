from monty.math import nCr, nPr


class TestFunc:
    def test_nCr(self):
        assert nCr(4, 2) == 6

    def test_deprecated_property(self):
        assert nPr(4, 2) == 12
