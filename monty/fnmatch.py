# coding: utf-8
"""This module provides support for Unix shell-style wildcards"""
from __future__ import unicode_literals, absolute_import

import fnmatch

from monty.string import list_strings


class WildCard(object):
    """
    This object provides an easy-to-use interface for filename matching with
    shell patterns (fnmatch).

    >>> w = WildCard("*.nc|*.pdf")
    >>> w.filter(["foo.nc", "bar.pdf", "hello.txt"])
    ['foo.nc', 'bar.pdf']

    >>> w.filter("foo.nc")
    ['foo.nc']
    """
    def __init__(self, wildcard, sep="|"):
        """
        Initializes a WildCard.

        Args:
            wildcard (str): String of tokens separated by sep. Each token
                represents a pattern.
            sep (str): Separator for shell patterns.
        """
        self.pats = ["*"]
        if wildcard:
            self.pats = wildcard.split(sep)

    def __str__(self):
        return "<%s, patterns = %s>" % (self.__class__.__name__, self.pats)

    def filter(self, names):
        """
        Returns a list with the names matching the pattern.
        """
        names = list_strings(names)

        fnames = []
        for f in names:
            for pat in self.pats:
                if fnmatch.fnmatch(f, pat):
                    fnames.append(f)

        return fnames

    def match(self, name):
        """
        Returns True if name matches one of the patterns.
        """
        for pat in self.pats:
            if fnmatch.fnmatch(name, pat):
                return True

        return False
