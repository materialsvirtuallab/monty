from __future__ import annotations

from monty.math import nCr, nPr


def test_nCr():
    assert nCr(4, 2) == 6


def test_nPr():
    assert nPr(4, 2) == 12
