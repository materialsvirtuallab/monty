"""
This module implements serialization support for common formats such as json
and yaml.
"""
import json
import os

try:
    from ruamel.yaml import YAML
except ImportError:
    YAML = None  # type: ignore

from monty.io import zopen
from monty.json import MontyDecoder, MontyEncoder
from monty.msgpack import default, object_hook

try:
    import msgpack
except ImportError:
    msgpack = None


def loadfn(fn, *args, fmt=None, **kwargs):
    r"""
    Loads json/yaml/msgpack directly from a filename instead of a
    File-like object. File may also be a BZ2 (".BZ2") or GZIP (".GZ", ".Z")
    compressed file.
    For YAML, ruamel.yaml must be installed. The file type is automatically
    detected from the file extension (case insensitive).
    YAML is assumed if the filename contains ".yaml" or ".yml".
    Msgpack is assumed if the filename contains ".mpk".
    JSON is otherwise assumed.

    Args:
        fn (str/Path): filename or pathlib.Path.
        *args: Any of the args supported by json/yaml.load.
        fmt (string): If specified, the fmt specified would be used instead
            of autodetection from filename. Supported formats right now are
            "json", "yaml" or "mpk".
        **kwargs: Any of the kwargs supported by json/yaml.load.

    Returns:
        (object) Result of json/yaml/msgpack.load.
    """

    if fmt is None:
        basename = os.path.basename(fn).lower()
        if ".mpk" in basename:
            fmt = "mpk"
        elif any(ext in basename for ext in (".yaml", ".yml")):
            fmt = "yaml"
        else:
            fmt = "json"

    if fmt == "mpk":
        if msgpack is None:
            raise RuntimeError("Loading of message pack files is not possible as msgpack-python is not installed.")
        if "object_hook" not in kwargs:
            kwargs["object_hook"] = object_hook
        with zopen(fn, "rb") as fp:
            return msgpack.load(fp, *args, **kwargs)  # pylint: disable=E1101
    else:
        with zopen(fn, "rt") as fp:
            if fmt == "yaml":
                if YAML is None:
                    raise RuntimeError("Loading of YAML files requires ruamel.yaml.")
                yaml = YAML()
                return yaml.load(fp, *args, **kwargs)
            if fmt == "json":
                if "cls" not in kwargs:
                    kwargs["cls"] = MontyDecoder
                return json.load(fp, *args, **kwargs)

            raise TypeError(f"Invalid format: {fmt}")


def dumpfn(obj, fn, *args, fmt=None, **kwargs):
    r"""
    Dump to a json/yaml directly by filename instead of a
    File-like object. File may also be a BZ2 (".BZ2") or GZIP (".GZ", ".Z")
    compressed file.
    For YAML, ruamel.yaml must be installed. The file type is automatically
    detected from the file extension (case insensitive). YAML is assumed if the
    filename contains ".yaml" or ".yml".
    Msgpack is assumed if the filename contains ".mpk".
    JSON is otherwise assumed.

    Args:
        obj (object): Object to dump.
        fn (str/Path): filename or pathlib.Path.
        *args: Any of the args supported by json/yaml.dump.
        **kwargs: Any of the kwargs supported by json/yaml.dump.

    Returns:
        (object) Result of json.load.
    """
    if fmt is None:
        basename = os.path.basename(fn).lower()
        if ".mpk" in basename:
            fmt = "mpk"
        elif any(ext in basename for ext in (".yaml", ".yml")):
            fmt = "yaml"
        else:
            fmt = "json"

    if fmt == "mpk":
        if msgpack is None:
            raise RuntimeError("Loading of message pack files is not possible as msgpack-python is not installed.")
        if "default" not in kwargs:
            kwargs["default"] = default
        with zopen(fn, "wb") as fp:
            msgpack.dump(obj, fp, *args, **kwargs)  # pylint: disable=E1101
    else:
        with zopen(fn, "wt") as fp:
            if fmt == "yaml":
                if YAML is None:
                    raise RuntimeError("Loading of YAML files requires ruamel.yaml.")
                yaml = YAML()
                yaml.dump(obj, fp, *args, **kwargs)
            elif fmt == "json":
                if "cls" not in kwargs:
                    kwargs["cls"] = MontyEncoder
                fp.write(json.dumps(obj, *args, **kwargs))
            else:
                raise TypeError(f"Invalid format: {fmt}")
