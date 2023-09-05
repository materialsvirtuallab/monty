"""
TODO: Modify unittest doc.
"""

import random
import sys

from monty.string import remove_non_ascii, unicode2str


def test_remove_non_ascii():
    s = "".join(chr(random.randint(0, 127)) for i in range(10))
    s += "".join(chr(random.randint(128, 150)) for i in range(10))
    clean = remove_non_ascii(s)
    assert len(clean) == 10


def test_unicode2str():
    if sys.version_info.major < 3:
        assert type(unicode2str("a")) == str
    else:
        assert type(unicode2str("a")) == str
