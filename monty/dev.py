"""
This module implements several useful functions and decorators that can be
particularly useful for developers. E.g., deprecating methods / classes, etc.
"""

from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'

import re
import logging
import datetime
import warnings
import os
import subprocess
import multiprocessing

from functools import wraps


logger = logging.getLogger(__name__)


def logged(level=logging.DEBUG):
    """
    Useful logging decorator. If a method is logged, the beginning and end of
    the method call will be logged at a pre-specified level.

    Args:
        level: Level to log method at. Defaults to DEBUG.
    """
    def wrap(f):
        _logger = logging.getLogger("{}.{}".format(f.__module__, f.__name__))

        def wrapped_f(*args, **kwargs):
            _logger.log(level, "Called at {} with args = {} and kwargs = {}"
                        .format(datetime.datetime.now(), args, kwargs))
            data = f(*args, **kwargs)
            _logger.log(level, "Done at {} with args = {} and kwargs = {}"
                        .format(datetime.datetime.now(), args, kwargs))
            return data

        return wrapped_f
    return wrap


def deprecated(replacement=None):
    """
    Decorator to mark classes or functions as deprecated,
    with a possible replacement.

    Args:
        replacement: A replacement class or method.

    Returns:
        Original function, but with a warning to use the updated class.
    """
    def wrap(old):
        def wrapped(*args, **kwargs):
            msg = "{} is deprecated".format(old.__name__)
            if replacement is not None:
                msg += "; use {} in {} instead.".format(
                    replacement.__name__, replacement.__module__)
            warnings.simplefilter('default')
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return old(*args, **kwargs)
        return wrapped
    return wrap


class requires(object):
    """
    Decorator to mark classes or functions as requiring a specified condition
    to be true. This can be used to present useful error messages for
    optional dependencies. For example, decorating the following code will
    check if scipy is present and if not, a runtime error will be raised if
    someone attempts to call the use_scipy function::

        try:
            import scipy
        except ImportError:
            scipy = None

        @requires(scipy is not None, "scipy is not present.")
        def use_scipy():
            print scipy.majver

    Args:
        condition: Condition necessary to use the class or function.
        message: A message to be displayed if the condition is not True.
    """
    def __init__(self, condition, message):
        self.condition = condition
        self.message = message

    def __call__(self, _callable):
        @wraps(_callable)
        def decorated(*args, **kwargs):
            if not self.condition:
                raise RuntimeError(self.message)
            return _callable(*args, **kwargs)
        return decorated


def get_ncpus():
    """
    Number of virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program. Return -1 if ncpus cannot be detected. Taken from:
    http://stackoverflow.com/questions/1006289/how-to-find-out-the-number-of-
    cpus-in-python
    """
    # Python 2.6+
    # May raise NonImplementedError
    try:
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))
        if res > 0:
            return res
    except (AttributeError, ValueError):
        pass

    # Windows
    try:
        res = int(os.environ['NUMBER_OF_PROCESSORS'])
        if res > 0:
            return res
    except (KeyError, ValueError):
        pass

    # jython
    try:
        from java.lang import Runtime
        runtime = Runtime.getRuntime()
        res = runtime.availableProcessors()
        if res > 0:
            return res
    except ImportError:
        pass

    # BSD
    try:
        sysctl = subprocess.Popen(['sysctl', '-n', 'hw.ncpu'],
                                  stdout=subprocess.PIPE)
        scstdout = sysctl.communicate()[0]
        res = int(scstdout)
        if res > 0:
            return res
    except (OSError, ValueError):
        pass

    # Linux
    try:
        res = open('/proc/cpuinfo').read().count('processor\t:')
        if res > 0:
            return res
    except IOError:
        pass

    # Solaris
    try:
        pseudo_devices = os.listdir('/devices/pseudo/')
        expr = re.compile('^cpuid@[0-9]+$')
        res = 0
        for pd in pseudo_devices:
            if expr.match(pd) is not None:
                res += 1
        if res > 0:
            return res
    except OSError:
        pass

    # Other UNIXes (heuristic)
    try:
        try:
            dmesg = open('/var/run/dmesg.boot').read()
        except IOError:
            dmesg_process = subprocess.Popen(['dmesg'], stdout=subprocess.PIPE)
            dmesg = dmesg_process.communicate()[0]

        res = 0
        while '\ncpu' + str(res) + ':' in dmesg:
            res += 1

        if res > 0:
            return res
    except OSError:
        pass

    logger.warning('Cannot determine number of CPUs on this system!')
    return -1
