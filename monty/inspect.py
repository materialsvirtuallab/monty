"""
Useful additional functions to help get information about live objects
"""

import inspect
import os
from inspect import currentframe, getframeinfo


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
    frame = currentframe()
    while True:
        if frame.f_back is None:
            finfo = getframeinfo(frame)
            return os.path.abspath(finfo.filename)

        frame = frame.f_back


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
        return ""
    parentframe = stack[start][0]

    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    # TODO(techtonik): consider using __main__
    if module:
        name.append(module.__name__)
    # detect classname
    if "self" in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals["self"].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != "<module>":  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)
