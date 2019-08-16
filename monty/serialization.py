"""
This module implements serialization support for common formats such as json
and yaml.
"""
from __future__ import absolute_import, unicode_literals

import json
import os
from monty.io import zopen
from monty.json import MontyEncoder, MontyDecoder
from monty.msgpack import default, object_hook

try:
    import ruamel.yaml as yaml
    try:  # Default to using CLoader and CDumper for speed.
        from ruamel.yaml import CLoader as Loader
        from ruamel.yaml import CDumper as Dumper
    except ImportError:
        from ruamel.yaml import Loader
        from ruamel.yaml import Dumper
except ImportError:
    try:
        import yaml
        try:  # Default to using CLoader and CDumper for speed.
            from yaml import CLoader as Loader
            from yaml import CDumper as Dumper
        except ImportError:
            from yaml import Loader
            from yaml import Dumper
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


def loadfn(fn, *args, fmt=None, **kwargs):
    """
    Loads json/yaml/msgpack directly from a filename instead of a
    File-like object. File may also be a BZ2 (".BZ2") or GZIP (".GZ", ".Z") compressed file.
    For YAML, ruamel.yaml must be installed. The file type is automatically detected
    from the file extension (case insensitive). YAML is assumed if the filename contains
    ".yaml" or ".yml". Msgpack is assumed if the filename contains ".mpk".
    JSON is otherwise assumed. The file type can be specified manually with "fmt='type'".

    Args:
        fn (str/Path): filename or pathlib.Path.
        \*args: Any of the args supported by json/yaml.load.
        fmt (str): manually specify file format to read.
            Options are "json", "yaml", or "mpk". If None, the
            file type will be detected automatically.
        \*\*kwargs: Any of the kwargs supported by json/yaml.load.

    Returns:
        (object) Result of json/yaml/msgpack.load.
    """
    if not fmt:
        basename = os.path.basename(fn).lower()
        if ".mpk" in basename:
            fmt = 'mpk'
        elif any(ext in basename for ext in (".yaml", ".yml")):
            fmt = 'yaml'
        else:
            fmt = 'json'

    if fmt == 'mpk':
        if msgpack is None:
            raise RuntimeError(
                "Loading of message pack files is not "
                "possible as msgpack-python is not installed.")
        if "object_hook" not in kwargs:
            kwargs["object_hook"] = object_hook
        with zopen(fn, "rb") as fp:
            return msgpack.load(fp, *args, **kwargs)
    else:
        with zopen(fn, 'rt') as fp:
            if fmt == 'yaml':
                if yaml is None:
                    raise RuntimeError("Loading of YAML files is not "
                                       "possible as ruamel.yaml is not installed.")
                if "Loader" not in kwargs:
                    kwargs["Loader"] = Loader
                return yaml.load(fp, *args, **kwargs)
            elif fmt == 'json':
                if "cls" not in kwargs:
                    kwargs["cls"] = MontyDecoder
                return json.load(fp, *args, **kwargs)
            else:
                raise TypeError("Invalid format: {}".format(fmt))


def dumpfn(obj, fn, *args, fmt=None, **kwargs):
    """
    Dump to a json/yaml directly by filename instead of a
    File-like object. File may also be a BZ2 (".BZ2") or GZIP (".GZ", ".Z") compressed file.
    For YAML, ruamel.yaml must be installed. The file type is automatically detected
    from the file extension (case insensitive). YAML is assumed if the filename contains
    ".yaml" or ".yml". Msgpack is assumed if the filename contains ".mpk".
    JSON is otherwise assumed. The file type can be specified manually with "fmt='type'".

    Args:
        obj (object): Object to dump.
        fn (str/Path): filename or pathlib.Path.
        \*args: Any of the args supported by json/yaml.dump.
        fmt (str): manually specify file format to read.
            Options are "json", "yaml", or "mpk". If None, the
            file type will be detected automatically.
        \*\*kwargs: Any of the kwargs supported by json/yaml.dump.

    Returns:
        (object) Result of json.load.
    """
    if not fmt:
        basename = os.path.basename(fn).lower()
        if ".mpk" in basename:
            fmt = 'mpk'
        elif any(ext in basename for ext in (".yaml", ".yml")):
            fmt = 'yaml'
        else:
            fmt = 'json'

    if fmt == 'mpk':
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
            if fmt == 'yaml':
                if yaml is None:
                    raise RuntimeError("Loading of YAML files is not "
                                       "possible as ruamel.yaml is not installed.")
                if "Dumper" not in kwargs:
                    kwargs["Dumper"] = Dumper
                yaml.dump(obj, fp, *args, **kwargs)
            elif fmt == 'json':
                if "cls" not in kwargs:
                    kwargs["cls"] = MontyEncoder
                fp.write("%s" % json.dumps(obj, *args, **kwargs))
            else:
                raise TypeError("Invalid format: {}".format(fmt))
