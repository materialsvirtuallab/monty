"""
Useful additional string functions.
"""

from __future__ import absolute_import


from __future__ import division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "2/28/14"


def remove_non_ascii(s):
    """
    Remove non-ascii characters in a file. Needed when support for non-ASCII
    is not available.

    Args:
        s: Input string

    Returns:
        String with all non-ascii characters removed.
    """
    return "".join(i for i in s if ord(i) < 128)