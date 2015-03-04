"""
Useful additional functions to help get information about live objects
"""
from __future__ import absolute_import, division, print_function, unicode_literals


def all_subclasses(cls):
    """
    Given a class `cls`, this recursive function returns a list with
    all subclasses, subclasses of subclasses, and so on.
    """
    subclasses = cls.__subclasses__() 
    return subclasses + [g for s in subclasses for g in all_subclasses(s)]


def find_top_pyfile():
    """
    This function inspects the Cpython frame to find the path of the script.
    """
    import os
    from inspect import currentframe, getframeinfo
    frame = currentframe()
    while True:
        if frame.f_back is None:
            finfo = getframeinfo(frame)
            #print(getframeinfo(frame))
            return os.path.abspath(finfo.filename)

        frame = frame.f_back
