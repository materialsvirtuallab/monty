"""
Math functions.
"""

from __future__ import absolute_import
from __future__ import division

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '8/6/14'

import fractions


def gcd(*numbers):
    """
    Returns the greatest common denominator for a sequence of numbers.

    Args:
        \*numbers: Sequence of numbers.
    """
    return reduce(fractions.gcd, numbers)


def lcm(*numbers):
    """
    Return lowest common multiple of a sequence of numbers.

    Args:
        \*numbers: Sequence of numbers.
    """
    def lcm(a, b):
        return (a * b) // gcd(a, b)

    return reduce(lcm, numbers, 1)