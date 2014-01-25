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


import logging
import datetime
import warnings
from functools import wraps


def logged(level=logging.DEBUG):
    """
    Useful logging decorator. If a method is logged, the beginning and end of
    the method call will be logged at a pre-specified level.

    Args:
        level: Level to log method at. Defaults to DEBUG.
    """
    def wrap(f):
        logger = logging.getLogger("{}.{}".format(f.__module__, f.__name__))

        def wrapped_f(*args, **kwargs):
            logger.log(level, "Called at {} with args = {} and kwargs = {}"
                       .format(datetime.datetime.now(), args, kwargs))
            data = f(*args, **kwargs)
            logger.log(level, "Done at {} with args = {} and kwargs = {}"
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

    def __call__(self, callable):
        @wraps(callable)
        def decorated(*args, **kwargs):
            if not self.condition:
                raise RuntimeError(self.message)
            return callable(*args, **kwargs)
        return decorated
