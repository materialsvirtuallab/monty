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


import json
from monty.io import zopen


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
    with zopen(f) as fp:
        return json.load(fp, *args, **kwargs)


def dumpf(obj, f, *args, **kwargs):
    """
    Dump to a json directly by filename instead of a File-like object.

    Args:
        obj (object): Object to dump.
        f (str): filename.
        \*args: Any of the args supported by Python's json.load.
        \*\*kwargs: Any of the kwargs supported by Python's json.load.

    Returns:
        (object) Result of json.load.
    """
    with zopen(f, "wb") as fp:
        json.dump(obj, fp, *args, **kwargs)