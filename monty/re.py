# coding: utf-8
"""
#TODO: Write module doc.
"""

from __future__ import division, unicode_literals, absolute_import

import re
from monty.io import zopen, reverse_readfile
import collections


__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '6/2/15'


def regrep(filename, patterns, reverse=False, terminate_on_match=False,
           postprocess=str):
    """
    A powerful regular expression version of grep.

    Args:
        filename (str): Filename to grep.
        patterns (dict): A dict of patterns, e.g.,
            {"energy": "energy\(sigma->0\)\s+=\s+([\d\-\.]+)"}.
        reverse (bool): Read files in reverse. Defaults to false. Useful for
            large files, especially when used with terminate_on_match.
        terminate_on_match (bool): Whether to terminate when there is at
            least one match in each key in pattern.
        postprocess (callable): A post processing function to convert all
            matches. Defaults to str, i.e., no change.

    Returns:
        A dict of the following form:
            {key1: [[[matches...], lineno], [[matches...], lineno],
                    [[matches...], lineno], ...],
            key2: ...}
        For reverse reads, the lineno is given as a -ve number. Please note
        that 0-based indexing is used.
    """
    compiled = {k: re.compile(v) for k, v in patterns.items()}
    matches = collections.defaultdict(list)
    gen = reverse_readfile(filename) if reverse else zopen(filename, "rt")
    for i, l in enumerate(gen):
        for k, p in compiled.items():
            m = p.search(l)
            if m:
                matches[k].append([[postprocess(g) for g in m.groups()],
                                   -i if reverse else i])
        if terminate_on_match and all([
                len(matches.get(k, [])) for k in compiled.keys()]):
            break
    try:
        # Try to close open file handle. Pass if it is a generator.
        gen.close()
    except:
        pass
    return matches
