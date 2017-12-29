"""
Useful additional functions for operators
"""
from __future__ import absolute_import, division, unicode_literals

import operator


def operator_from_str(op):
    """
    Return the operator associated to the given string `op`.

    raises:
        `KeyError` if invalid string.

    >>> assert operator_from_str("==")(1, 1) and operator_from_str("+")(1,1) == 2
    """
    d = {"==": operator.eq,
         "!=": operator.ne,
         ">": operator.gt,
         ">=": operator.ge,
         "<": operator.lt,
         "<=": operator.le,
         '+': operator.add,
         '-': operator.sub,
         '*': operator.mul,
         '%': operator.mod,
         '^': operator.xor,
         }

    try:
        d['/'] = operator.truediv
    except AttributeError:
        pass

    return d[op]
