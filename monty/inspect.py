"""
Useful additional functions to help get information about live objects
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
from inspect import currentframe, getframeinfo, stack, getouterframes


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
    #from inspect import currentframe, getframeinfo
    frame = currentframe()
    while True:
        if frame.f_back is None:
            finfo = getframeinfo(frame)
            #print(getframeinfo(frame))
            return os.path.abspath(finfo.filename)

        frame = frame.f_back


def find_caller():
    """
    Find the stack frame of the caller so that we can note the source file name, 
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

    import collections
    # See also
    #http://stackoverflow.com/questions/2654113/python-how-to-get-the-callers-method-name-in-the-called-method

    CallerInfo = collections.namedtuple("CallerInfo", "filename, lineno, name")
    caller = CallerInfo("(unknown file)", 0, "(unknown function)")

    curframe = currentframe()
    if curframe is None:
        return caller

    f = getouterframes(curframe, 2)[1][0]
    #print(f)

    import sys, os
    co = f.f_code
    filename = os.path.normcase(co.co_filename)
    return CallerInfo(co.co_filename, f.f_lineno, co.co_name)

    #print('caller name:', calframe[1][3])
    #_getframe = currentframe
    # _srcfile is used when walking the stack to check when we've got the first caller stack frame.

    if hasattr(sys, 'frozen'): #support for py2exe
        _srcfile = "logging%s__init__%s" % (os.sep, __file__[-4:])
    elif __file__[-4:].lower() in ['.pyc', '.pyo']:
        _srcfile = __file__[:-4] + '.py'
    else:
        _srcfile = __file__
    #print(_srcfile)

    _srcfile = os.path.normcase(_srcfile)

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


def caller_name(skip=2):
    """
    Get a name of a caller in the format module.class.method
    
    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.
       
    An empty string is returned if skipped levels exceed stack height

    Taken from:

        https://gist.github.com/techtonik/2151727

    Public Domain, i.e. feel free to copy/paste
    """
    stack = inspect.stack()
    start = 0 + skip
    if len(stack) < start + 1:
      return ''
    parentframe = stack[start][0]    
    
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append( codename ) # function or a method
    del parentframe
    return ".".join(name)


def initializer(func):
    """
    Automatically assigns the parameters.
    http://stackoverflow.com/questions/1389180/python-automatically-initialize-instance-variables

    >>> class process:
    ...     @initializer
    ...     def __init__(self, cmd, reachable=False, user='root'):
    ...         pass
    >>> p = process('halt', True)
    >>> p.cmd, p.reachable, p.user
    ('halt', True, 'root')
    """
    names, varargs, keywords, defaults = inspect.getargspec(func)

    from functools import wraps
    @wraps(func)
    def wrapper(self, *args, **kargs):
        #print("names", names, "defaults", defaults)
        for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
            setattr(self, name, arg)

        # Avoid TypeError: argument to reversed() must be a sequence
        if defaults is not None:
            for name, default in zip(reversed(names), reversed(defaults)):
                if not hasattr(self, name):
                    setattr(self, name, default)

        return func(self, *args, **kargs)

    return wrapper

