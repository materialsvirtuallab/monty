"""
This module implements serialization support for common formats such as json
and yaml.
"""
from __future__ import absolute_import, unicode_literals

import json
from monty.io import zopen
from monty.json import MontyEncoder, MontyDecoder
from monty.msgpack import default, object_hook

try:
    import ruamel.yaml as yaml
except ImportError:
    try:
        import yaml
    except ImportError:
        yaml = None

try:
    import msgpack
except ImportError:
    msgpack = None

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '7/29/14'


def loadfn(fn, *args, **kwargs):
    """
    Loads json/yaml/msgpack directly from a filename instead of a
    File-like object. For YAML, ruamel.yaml must be installed. The file type is
    automatically detected. YAML is assumed if the filename contains "yaml"
    (lower or upper case). Otherwise, json is always assumed.

    Args:
        fn (str/Path): filename or pathlib.Path.
        \*args: Any of the args supported by json/yaml.load.
        \*\*kwargs: Any of the kwargs supported by json/yaml.load.

    Returns:
        (object) Result of json/yaml/msgpack.load.
    """
    if "mpk" in fn.lower():
        if msgpack is None:
            raise RuntimeError(
                "Loading of message pack files is not "
                "possible as msgpack-python is not installed.")
        if "object_hook" not in kwargs:
            kwargs["object_hook"] = object_hook
        with zopen(fn, "rb") as fp:
            return msgpack.load(fp, *args, **kwargs)
    else:
        with zopen(fn) as fp:
            if "yaml" in fn.lower():
                if yaml is None:
                    raise RuntimeError("Loading of YAML files is not "
                                       "possible as ruamel.yaml is not installed.")
                return yaml.safe_load(fp, *args, **kwargs)
            else:
                if "cls" not in kwargs:
                    kwargs["cls"] = MontyDecoder
                return json.load(fp, *args, **kwargs)


def dumpfn(obj, fn, *args, **kwargs):
    """
    Dump to a json/yaml directly by filename instead of a File-like object.
    For YAML, ruamel.yaml must be installed. The file type is automatically
    detected. YAML is assumed if the filename contains "yaml" (lower or upper
    case). Otherwise, json is always assumed.

    Args:
        obj (object): Object to dump.
        fn (str/Path): filename or pathlib.Path.
        \*args: Any of the args supported by json/yaml.dump.
        \*\*kwargs: Any of the kwargs supported by json/yaml.dump.

    Returns:
        (object) Result of json.load.
    """
    if "mpk" in fn.lower():
        if msgpack is None:
            raise RuntimeError(
                "Loading of message pack files is not "
                "possible as msgpack-python is not installed.")
        if "default" not in kwargs:
            kwargs["default"] = default
        with zopen(fn, "wb") as fp:
            msgpack.dump(obj, fp, *args, **kwargs)
    else:
        with zopen(fn, "wt") as fp:
            if "yaml" in fn.lower():
                if yaml is None:
                    raise RuntimeError("Loading of YAML files is not "
                                       "possible as ruamel.yaml is not installed.")
                yaml.safe_dump(obj, fp, *args, **kwargs)
            else:
                if "cls" not in kwargs:
                    kwargs["cls"] = MontyEncoder
                fp.write("%s" % json.dumps(obj, *args, **kwargs))
