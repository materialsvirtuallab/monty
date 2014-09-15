"""
Useful additional string functions.
"""

from __future__ import absolute_import, division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "ongsp@ucsd.edu"
__date__ = "2/28/14"


import sys


def remove_non_ascii(s):
    """
    Remove non-ascii characters in a file. Needed when support for non-ASCII
    is not available.

    Args:
        s (str): Input string

    Returns:
        String with all non-ascii characters removed.
    """
    return "".join(i for i in s if ord(i) < 128)


def unicode2str(s):
    """
    Forces a unicode to a string in Python 2, but transparently handles
    Python 3.

    Args:
        s (str/unicode): Input string / unicode.

    Returns:
        str in Python 2. Unchanged otherwise.
    """
    return s.encode('utf-8') if sys.version_info.major < 3 else s


def str2unicode(s):
    """
    Converts strings to unicode in python 2. Ignores Python 3 strings.

    Args:
        s (str/unicode): Input string / unicode.

    Returns:
        Unicode.
    """
    return unicode(s) if sys.version_info.major < 3 else s


def marquee(text="", width=78, mark='*'):
    """
    Return the input string centered in a 'marquee'.

    Args:
        text (str): Input string
        width (int): Width of final output string.
        mark (str): Character used to fill string.

    :Examples:

    >>> marquee('A test', width=40)
    '**************** A test ****************'

    >>> marquee('A test', width=40, mark='-')
    '---------------- A test ----------------'

    marquee('A test',40, ' ')
    '                 A test                 '
    """
    if not text:
        return (mark*width)[:width]

    nmark = (width-len(text)-2)//len(mark)//2
    if nmark < 0: 
        nmark = 0

    marks = mark * nmark
    return '%s %s %s' % (marks, text, marks)
