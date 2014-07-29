"""
This module implements serialization support for common formats such as json
and yaml.
"""
from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '7/29/14'


import json
from monty.io import zopen
try:
    import yaml
    # Use CLoader for faster performance where possible.
    try:
        from yaml import CLoader as Loader
    except ImportError:
        from yaml import Loader
except ImportError:
    yaml = None
    Loader = None


def serial_loadf(f, *args, **kwargs):
    """
    Loads json/yaml directly from a filename instead of a File-like object.
    For YAML, PyYAML must be installed. The file type is automatically
    detected. YAML is assumed if the filename contains "yaml" (lower or upper
    case). Otherwise, json is always assumed.

    Args:
        f (str): filename
        \*args: Any of the args supported by Python's json.load.
        \*\*kwargs: Any of the kwargs supported by Python's json.load.

    Returns:
        (object) Result of json/yaml.load.
    """
    with zopen(f) as fp:
        serial_mod = json
        if "yaml" in f.lower():
            if yaml is None:
                raise RuntimeError("Loading of YAML files is not "
                                   "possible as PyYAML is not installed.")
            serial_mod = yaml
        return serial_mod.load(fp, *args, **kwargs)


def serial_dumpf(obj, f, *args, **kwargs):
    """
    Dump to a json/yaml directly by filename instead of a File-like object.
    For YAML, PyYAML must be installed. The file type is automatically
    detected. YAML is assumed if the filename contains "yaml" (lower or upper
    case). Otherwise, json is always assumed.
    
    Args:
        obj (object): Object to dump.
        f (str): filename.
        \*args: Any of the args supported by Python's json.load.
        \*\*kwargs: Any of the kwargs supported by Python's json.load.

    Returns:
        (object) Result of json.load.
    """
    with open(f, "wt") as fp:
        serial_mod = json
        if "yaml" in f.lower():
            if yaml is None:
                raise RuntimeError("Loading of YAML files is not "
                                   "possible as PyYAML is not installed.")
            serial_mod = yaml
        return serial_mod.dump(obj, fp, *args, **kwargs)
