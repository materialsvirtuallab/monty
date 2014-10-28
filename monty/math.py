# coding: utf-8

from __future__ import division, unicode_literals, absolute_import

"""
Addition math functions.
"""

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '10/28/14'


import math


def nCr(n, r):
    """
    Calculates nCr.

    Args:
        n (int): total number of items.
        r (int): items to choose

    Returns:
        nCr.
    """
    f = math.factorial
    return int(f(n) / f(r) / f(n-r))


def nPr(n, r):
    """
    Calculates nPr.

    Args:
        n (int): total number of items.
        r (int): items to permute

    Returns:
        nPr.
    """
    f = math.factorial
    return int(f(n) / f(n-r))
