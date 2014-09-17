#!/usr/bin/env python

"""
TODO: Modify module doc.
"""
from __future__ import absolute_import, division

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2012, The Materials Project"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "9/13/14"


import logging
import datetime
import functools


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


def enable_logging(main):
    """
    This decorator is used to decorate main functions.
    It adds the initialization of the logger and an argument parser that allows
    one to select the loglevel.
    Useful if we are writing simple main functions that call libraries where
    the logging module is used

    Args:
        main:
            main function.
    """
    @functools.wraps(main)
    def wrapper(*args, **kwargs):
        import argparse
        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--loglevel', default="ERROR", type=str,
            help="Set the loglevel. Possible values: CRITICAL, ERROR (default),"
                 "WARNING, INFO, DEBUG")

        options = parser.parse_args()

        # loglevel is bound to the string value obtained from the command line
        # argument.
        # Convert to upper case to allow the user to specify --loglevel=DEBUG
        # or --loglevel=debug
        numeric_level = getattr(logging, options.loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % options.loglevel)
        logging.basicConfig(level=numeric_level)

        retcode = main(*args, **kwargs)
        return retcode

    return wrapper
