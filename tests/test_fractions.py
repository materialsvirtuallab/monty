import pytest

from monty.fractions import gcd, gcd_float, lcm


def test_gcd():
    assert gcd(7, 14, 63) == 7


def test_lcm():
    assert lcm(2, 3, 4) == 12


def test_gcd_float():
    vs = [6.2, 12.4, 15.5 + 5e-9]
    assert gcd_float(vs, 1e-8) == pytest.approx(3.1)
