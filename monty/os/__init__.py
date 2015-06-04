from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'

import os

from contextlib import contextmanager


@contextmanager
def cd(path):
    """
    A Fabric-inspired cd context that temporarily changes directory for
    performing some tasks, and returns to the original working directory
    afterwards. E.g.,

        with cd("/my/path/"):
            do_something()

    Args:
        path: Path to cd to.
    """
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)