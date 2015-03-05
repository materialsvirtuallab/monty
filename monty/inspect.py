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



def find_caller():
    """
    find the stack frame of the caller so that we can note the source file name, 
    line number and function name.

    Return:
        `namedtuple` with the following attributes:

        ===========  ==================================================
        filename     name of file in which this code object was created
        lineno       current line number in Python source code
        name         name with which this code object was defined
        ===========  ==================================================
    """
    # next bit filched from 1.5.2's inspect.py
    #def currentframe():
    #    """Return the frame object for the caller's stack frame."""
    #    try:
    #        raise Exception
    #    except:
    #        return sys.exc_info()[2].tb_frame.f_back

    # CPython implementation detail: This function should be used for internal and specialized purposes only. 
    # It is not guaranteed to exist in all implementations of Python.
    #if hasattr(sys, '_getframe'): currentframe = lambda: sys._getframe(3)
    # done filching

    from inspect import currentframe
    #_getframe = currentframe

    # _srcfile is used when walking the stack to check when we've got the first caller stack frame.
    import sys, os
    if hasattr(sys, 'frozen'): #support for py2exe
        _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
    elif __file__[-4:].lower() in ['.pyc', '.pyo']:
        _srcfile = __file__[:-4] + '.py'
    else:
        _srcfile = __file__
    #print(_srcfile)

    _srcfile = os.path.normcase(_srcfile)

    import collections
    CallerInfo = collections.namedtuple("CallerInfo", "filename, lineno, name")
    caller = CallerInfo("(unknown file)", 0, "(unknown function)")

    f = currentframe()
    # On some versions of IronPython, currentframe() returns None if
    # IronPython isn't run with -X:Frames.
    if f is None:
        return caller

    f = f.f_back
    while hasattr(f, "f_code"):
        co = f.f_code
        filename = os.path.normcase(co.co_filename)
        if filename == _srcfile:
            f = f.f_back
            continue
        caller = CallerInfo(co.co_filename, f.f_lineno, co.co_name)
        break

    return caller
