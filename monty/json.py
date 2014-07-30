"""
JSON serialization and deserialization utilities.
"""

from __future__ import absolute_import

__author__ = "Shyue Ping Ong"
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = "0.1"
__maintainer__ = "Shyue Ping Ong"
__email__ = "shyuep@gmail.com"
__date__ = "1/24/14"


from monty.dev import deprecated
from monty.serialization import loadfn, dumpfn


@deprecated(replacement=loadfn)
def loadf(f, *args, **kwargs):
    """
    Load json directly from a filename instead of a File-like object.

    Args:
        f (str): filename
        \*args: Any of the args supported by Python's json.load.
        \*\*kwargs: Any of the kwargs supported by Python's json.load.

    Returns:
        (object) Result of json.load.
    """
    return loadfn(f, *args, **kwargs)


@deprecated(replacement=dumpfn)
def dumpf(obj, f, *args, **kwargs):
    """
    Dump to a json directly by filename instead of a File-like object.

    Args:
        obj (object): Object to dump.
        f (str): filename.
        \*args: Any of the args supported by Python's json.load.
        \*\*kwargs: Any of the kwargs supported by Python's json.load.
    """
    dumpfn(obj, f, *args, **kwargs)