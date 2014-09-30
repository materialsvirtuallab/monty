"""
This module implements serialization support for common formats such as json
and yaml.
"""
from __future__ import absolute_import, unicode_literals

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
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
except ImportError:
    yaml = None
    Loader = None


def loadfn(fn, *args, **kwargs):
    """
    Loads json/yaml directly from a filename instead of a File-like object.
    For YAML, PyYAML must be installed. The file type is automatically
    detected. YAML is assumed if the filename contains "yaml" (lower or upper
    case). Otherwise, json is always assumed. Furthermore, if pyyaml is
    compiled with the LibYAML library, the CLoader is automatically chosen
    for ~10x faster parsing.

    Args:
        fn (str): filename
        \*args: Any of the args supported by json/yaml.load.
        \*\*kwargs: Any of the kwargs supported by json/yaml.load.

    Returns:
        (object) Result of json/yaml.load.
    """
    with zopen(fn) as fp:
        if "yaml" in fn.lower():
            if yaml is None:
                raise RuntimeError("Loading of YAML files is not "
                                   "possible as PyYAML is not installed.")
            if "Loader" not in kwargs:
                kwargs["Loader"] = Loader
            return yaml.load(fp, *args, **kwargs)
        else:
            return json.load(fp, *args, **kwargs)


def dumpfn(obj, fn, *args, **kwargs):
    """
    Dump to a json/yaml directly by filename instead of a File-like object.
    For YAML, PyYAML must be installed. The file type is automatically
    detected. YAML is assumed if the filename contains "yaml" (lower or upper
    case). Otherwise, json is always assumed. Furthermore, if pyyaml is
    compiled with the LibYAML library, the CDumper is automatically chosen
    for ~10x faster parsing.

    Args:
        obj (object): Object to dump.
        fn (str): filename.
        \*args: Any of the args supported by json/yaml.dump.
        \*\*kwargs: Any of the kwargs supported by json/yaml.dump.

    Returns:
        (object) Result of json.load.
    """
    with zopen(fn, "wt") as fp:
        if "yaml" in fn.lower():
            if yaml is None:
                raise RuntimeError("Loading of YAML files is not "
                                   "possible as PyYAML is not installed.")
            if "Dumper" not in kwargs:
                kwargs["Dumper"] = Dumper
            yaml.dump(obj, fp, *args, **kwargs)
        else:
            fp.write("%s" % json.dumps(obj, *args, **kwargs))
