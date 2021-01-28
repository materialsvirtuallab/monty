# coding: utf-8
"""
JSON serialization and deserialization utilities.
"""

import os
import json
import datetime
import sys

from hashlib import sha1
from collections import OrderedDict, defaultdict
from collections import namedtuple
from enum import Enum
from typing import NamedTuple

from importlib import import_module

from inspect import getfullargspec

try:
    import numpy as np
except ImportError:
    np = None  # type: ignore

try:
    import bson
except ImportError:
    bson = None

try:
    import ruamel.yaml as yaml
except ImportError:
    try:
        import yaml  # type: ignore
    except ImportError:
        yaml = None  # type: ignore

from monty.collections import is_namedtuple
from monty.collections import is_NamedTuple


__version__ = "3.0.0"


def _load_redirect(redirect_file):
    try:
        with open(redirect_file, "rt") as f:
            d = yaml.safe_load(f)
    except IOError:
        # If we can't find the file
        # Just use an empty redirect dict
        return {}

    # Convert the full paths to module/class
    redirect_dict = defaultdict(dict)
    for old_path, new_path in d.items():
        old_class = old_path.split(".")[-1]
        old_module = ".".join(old_path.split(".")[:-1])

        new_class = new_path.split(".")[-1]
        new_module = ".".join(new_path.split(".")[:-1])

        redirect_dict[old_module][old_class] = {
            "@module": new_module,
            "@class": new_class,
        }

    return dict(redirect_dict)


# (Private) helper methods and variables for the serialization of
#  types for typing.NamedTuple's.
_typ2name = {typ: typ.__name__ for typ in (bool, int, float, complex,
                                           list, tuple, range,
                                           str,
                                           bytes, bytearray, memoryview,
                                           set, frozenset,
                                           dict)}
_name2typ = {val: key for key, val in _typ2name.items()}
_name2typ['NoneType'] = type(None)


def _serialize_type(typ):
    """Serialization of types."""
    # Builtin standard types
    if typ in _typ2name:
        return{"@module": "@builtins",
               "@class": "@types",
               "type": _typ2name[typ]}
    # None/NoneType is a special case
    if typ is type(None) or typ is None:  # noqa - disable pycodestyle check here
        return {"@module": "@builtins",
                "@class": "@types",
                "type": "NoneType"}
    # Other types ("normal" classes)
    return {"@module": "@builtins",
            "@class": "@types",
            "type": "@class",
            "type_module": typ.__module__,
            "type_class": typ.__name__}


def _deserialize_type(d):
    """Deserialization of types."""
    if d["type"] in _name2typ:
        return _name2typ[d["type"]]
    if d["type"] == "@class":
        modname = d["type_module"]
        classname = d["type_class"]
        if classname in MSONable.REDIRECT.get(modname, {}):
            modname = MSONable.REDIRECT[modname][classname]["@module"]
            classname = MSONable.REDIRECT[modname][classname]["@class"]
        mod = __import__(modname, globals(), locals(), [classname], 0)
        try:
            return getattr(mod, classname)
        except AttributeError:
            raise ValueError('Could not deserialize type.')
    raise ValueError('Could not deserialize type.')


def _recursive_as_dict(obj):
    """Recursive function to prepare serialization of objects.

    Takes care of tuples, namedtuples, OrderedDict, objects with an as_dict method.
    """
    if is_namedtuple(obj):
        d = {"namedtuple_as_list": [_recursive_as_dict(it) for it in obj],
             "fields": obj._fields,
             "typename": obj.__class__.__name__,
             "@module": "@builtins",
             "@class": "collections.namedtuple"}
        if sys.version_info >= (3, 7):  # default values for collections.namedtuple's were introduced in python 3.7.
            d["fields_defaults"] = obj._fields_defaults
        return d
    if is_NamedTuple(obj):
        d = {"NamedTuple_as_list": [_recursive_as_dict(it) for it in obj],
             "fields": obj._fields,
             "fields_types": [_serialize_type(obj._field_types[field]) for field in obj._fields],
             "typename": obj.__class__.__name__,
             "doc": obj.__doc__,
             "@module": "@builtins",
             "@class": "typing.NamedTuple"}
        if sys.version_info >= (3, 6):  # default values for typing.NamedTuple's were introduced in python 3.6.
            try:
                d["fields_defaults"] = [(field, _recursive_as_dict(field_default))
                                        for field, field_default in obj._field_defaults.items()]
            except AttributeError:
                d["fields_defaults"] = []
        return d
    # The order of the ifs matter here as namedtuples and NamedTuples are instances (subclasses) of tuples,
    # same for OrderedDict which is an instance (subclass) of dict.
    if isinstance(obj, set):
        return {"set_as_list": [_recursive_as_dict(it) for it in obj],
                "@module": "@builtins",
                "@class": "set"}
    if isinstance(obj, tuple):
        return {"tuple_as_list": [_recursive_as_dict(it) for it in obj],
                "@module": "@builtins",
                "@class": "tuple"}
    if isinstance(obj, OrderedDict):
        return {"ordereddict_as_list": [[key, _recursive_as_dict(val)] for key, val in obj.items()],
                "@module": "@builtins",
                "@class": "OrderedDict"}
    if isinstance(obj, list):
        return [_recursive_as_dict(it) for it in obj]
    if isinstance(obj, dict):
        return {kk: _recursive_as_dict(vv) for kk, vv in obj.items()}
    if hasattr(obj, "as_dict"):
        return obj.as_dict()
    return obj


class MSONable:
    """
    This is a mix-in base class specifying an API for msonable objects. MSON
    is Monty JSON. Essentially, MSONable objects must implement an as_dict
    method, which must return a json serializable dict and must also support
    no arguments (though optional arguments to finetune the output is ok),
    and a from_dict class method that regenerates the object from the dict
    generated by the as_dict method. The as_dict method should contain the
    "@module" and "@class" keys which will allow the MontyEncoder to
    dynamically deserialize the class. E.g.::

        d["@module"] = self.__class__.__module__
        d["@class"] = self.__class__.__name__

    A default implementation is provided in MSONable, which automatically
    determines if the class already contains self.argname or self._argname
    attributes for every arg. If so, these will be used for serialization in
    the dict format. Similarly, the default from_dict will deserialization
    classes of such form. An example is given below::

        class MSONClass(MSONable):

        def __init__(self, a, b, c, d=1, **kwargs):
            self.a = a
            self.b = b
            self._c = c
            self._d = d
            self.kwargs = kwargs

    For such classes, you merely need to inherit from MSONable and you do not
    need to implement your own as_dict or from_dict protocol.

    New to Monty V2.0.6....
    Classes can be redirected to moved implementations by putting in the old
    fully qualified path and new fully qualified path into .monty.yaml in the
    home folder

    Example:
    old_module.old_class: new_module.new_class
    """

    REDIRECT = _load_redirect(
        os.path.join(os.path.expanduser("~"), ".monty.yaml"))

    def as_dict(self) -> dict:
        """
        A JSON serializable dict representation of an object.
        """
        d = {
            "@module": self.__class__.__module__,
            "@class": self.__class__.__name__
        }

        try:
            parent_module = self.__class__.__module__.split('.')[0]
            module_version = import_module(parent_module).__version__  # type: ignore
            d["@version"] = u"{}".format(module_version)
        except (AttributeError, ImportError):
            d["@version"] = None  # type: ignore

        spec = getfullargspec(self.__class__.__init__)
        args = spec.args

        for c in args:
            if c != "self":
                try:
                    a = self.__getattribute__(c)
                except AttributeError:
                    try:
                        a = self.__getattribute__("_" + c)
                    except AttributeError:
                        raise NotImplementedError(
                            "Unable to automatically determine as_dict "
                            "format from class. MSONAble requires all "
                            "args to be present as either self.argname or "
                            "self._argname, and kwargs to be present under"
                            "a self.kwargs variable to automatically "
                            "determine the dict format. Alternatively, "
                            "you can implement both as_dict and from_dict.")
                d[c] = _recursive_as_dict(a)
        if hasattr(self, "kwargs"):
            # type: ignore
            d.update(**getattr(self, "kwargs"))  # pylint: disable=E1101
        if spec.varargs is not None and getattr(self, spec.varargs, None) is not None:
            d.update({spec.varargs: getattr(self, spec.varargs)})
        if hasattr(self, "_kwargs"):
            d.update(**getattr(self, "_kwargs"))  # pylint: disable=E1101
        if isinstance(self, Enum):
            d.update({"value": self.value})  # pylint: disable=E1101
        return d

    @classmethod
    def from_dict(cls, d):
        """
        :param d: Dict representation.
        :return: MSONable class.
        """
        decoded = {
            k: MontyDecoder().process_decoded(v)
            for k, v in d.items() if not k.startswith("@")
        }
        return cls(**decoded)

    def to_json(self) -> str:
        """
        Returns a json string representation of the MSONable object.
        """
        return json.dumps(self, cls=MontyEncoder)

    def unsafe_hash(self):
        """
        Returns an hash of the current object. This uses a generic but low
        performance method of converting the object to a dictionary, flattening
        any nested keys, and then performing a hash on the resulting object
        """

        def flatten(obj, seperator="."):
            # Flattens a dictionary

            flat_dict = {}
            for key, value in obj.items():
                if isinstance(value, dict):
                    flat_dict.update({
                        seperator.join([key, _key]): _value
                        for _key, _value in flatten(value).items()
                    })
                elif isinstance(value, list):
                    list_dict = {
                        "{}{}{}".format(key, seperator, num): item
                        for num, item in enumerate(value)
                    }
                    flat_dict.update(flatten(list_dict))
                else:
                    flat_dict[key] = value

            return flat_dict

        ordered_keys = sorted(flatten(jsanitize(self.as_dict())).items(),
                              key=lambda x: x[0])
        ordered_keys = [item for item in ordered_keys if "@" not in item[0]]
        return sha1(json.dumps(OrderedDict(ordered_keys)).encode("utf-8"))


class MontyEncoder(json.JSONEncoder):
    """
    A Json Encoder which supports the MSONable API, plus adds support for
    numpy arrays, datetime objects, bson ObjectIds (requires bson).

    Usage::

        # Add it as a *cls* keyword when using json.dump
        json.dumps(object, cls=MontyEncoder)
    """

    def default(self, o) -> dict:  # pylint: disable=E0202
        """
        Overriding default method for JSON encoding. This method does two
        things: (a) If an object has a to_dict property, return the to_dict
        output. (b) If the @module and @class keys are not in the to_dict,
        add them to the output automatically. If the object has no to_dict
        property, the default Python json encoder default method is called.

        Args:
            o: Python object.

        Return:
            Python dict representation.
        """
        if isinstance(o, datetime.datetime):
            return {
                "@module": "datetime",
                "@class": "datetime",
                "string": o.__str__()
            }
        if np is not None:
            if isinstance(o, np.ndarray):
                if str(o.dtype).startswith('complex'):
                    return {
                        "@module": "numpy",
                        "@class": "array",
                        "dtype": o.dtype.__str__(),
                        "data": [o.real.tolist(),
                                 o.imag.tolist()]
                    }
                return {
                    "@module": "numpy",
                    "@class": "array",
                    "dtype": o.dtype.__str__(),
                    "data": o.tolist()
                }
            if isinstance(o, np.generic):
                return o.item()
        if bson is not None:
            if isinstance(o, bson.objectid.ObjectId):
                return {
                    "@module": "bson.objectid",
                    "@class": "ObjectId",
                    "oid": str(o)
                }

        # Is this still useful as we are now calling the _recursive_as_dict
        #  method (which takes care of as_dict's) before the encoding ?
        try:
            d = o.as_dict()
            if "@module" not in d:
                d["@module"] = u"{}".format(o.__class__.__module__)
            if "@class" not in d:
                d["@class"] = u"{}".format(o.__class__.__name__)
            if "@version" not in d:
                try:
                    parent_module = o.__class__.__module__.split('.')[0]
                    module_version = import_module(parent_module).__version__  # type: ignore
                    d["@version"] = u"{}".format(module_version)
                except (AttributeError, ImportError):
                    d["@version"] = None
            return d
        except AttributeError:
            return json.JSONEncoder.default(self, o)

    def encode(self, o):
        """MontyEncoder's encode method.

        First, prepares the object by recursively transforming tuples, namedtuples,
        object having an as_dict method and others to encodable python objects.
        """
        # This cannot go in the default method because default is called as a last resort,
        # such that tuples and namedtuples have already been transformed to lists by json's encode method.
        o = _recursive_as_dict(o)
        return super().encode(o)


class MontyDecoder(json.JSONDecoder):
    """
    A Json Decoder which supports the MSONable API. By default, the
    decoder attempts to find a module and name associated with a dict. If
    found, the decoder will generate a Pymatgen as a priority.  If that fails,
    the original decoded dictionary from the string is returned. Note that
    nested lists and dicts containing pymatgen object will be decoded correctly
    as well.

    Usage:

        # Add it as a *cls* keyword when using json.load
        json.loads(json_string, cls=MontyDecoder)
    """

    def process_decoded(self, d):
        """
        Recursive method to support decoding dicts and lists containing
        pymatgen objects.
        """
        if isinstance(d, dict):
            if "@module" in d and "@class" in d:
                modname = d["@module"]
                classname = d["@class"]
                if classname in MSONable.REDIRECT.get(modname, {}):
                    modname = MSONable.REDIRECT[modname][classname]["@module"]
                    classname = MSONable.REDIRECT[modname][classname]["@class"]
            else:
                modname = None
                classname = None
            if modname and modname not in ["bson.objectid", "numpy"]:
                if modname == "datetime" and classname == "datetime":
                    try:
                        dt = datetime.datetime.strptime(
                            d["string"], "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        dt = datetime.datetime.strptime(
                            d["string"], "%Y-%m-%d %H:%M:%S")
                    return dt
                if modname == "@builtins":
                    if classname == "tuple":
                        return tuple([self.process_decoded(item) for item in d['tuple_as_list']])
                    if classname == "set":
                        return {self.process_decoded(item) for item in d['set_as_list']}
                    if classname == "collections.namedtuple":
                        # default values for collections.namedtuple have been introduced in python 3.7
                        # it is probably not essential to deserialize the defaults if the object was serialized with
                        # python >= 3.7 and deserialized with python < 3.7.
                        if sys.version_info < (3, 7):
                            nt = namedtuple(d['typename'], d['fields'])
                        else:
                            nt = namedtuple(d['typename'], d['fields'],  # pylint: disable=E1123
                                            defaults=d['fields_defaults'])  # pylint: disable=E1123
                        return nt(*[self.process_decoded(item) for item in d['namedtuple_as_list']])
                    if classname == "typing.NamedTuple":
                        NT = NamedTuple(d['typename'], [(field, _deserialize_type(field_type))
                                                        for field, field_type in zip(d['fields'], d['fields_types'])])
                        NT.__doc__ = d['doc']
                        # default values for typing.NamedTuple have been introduced in python 3.6
                        if sys.version_info >= (3, 6):
                            NT._field_defaults = OrderedDict([(field, self.process_decoded(default))
                                                              for field, default in d['fields_defaults']])
                        return NT(*[self.process_decoded(item)  # pylint: disable=E1102
                                    for item in d['NamedTuple_as_list']])  # pylint: disable=E1102
                    if classname == "OrderedDict":
                        return OrderedDict([(key, self.process_decoded(val))
                                            for key, val in d['ordereddict_as_list']])

                mod = __import__(modname, globals(), locals(), [classname], 0)
                if hasattr(mod, classname):
                    cls_ = getattr(mod, classname)
                    data = {
                        k: v
                        for k, v in d.items() if not k.startswith("@")
                    }
                    if hasattr(cls_, "from_dict"):
                        return cls_.from_dict(data)
            elif np is not None and modname == "numpy" and classname == "array":
                if d["dtype"].startswith('complex'):
                    return np.array([
                        np.array(r) + np.array(i) * 1j
                        for r, i in zip(*d["data"])], dtype=d["dtype"])
                return np.array(d["data"], dtype=d["dtype"])

            elif (bson is not None) and modname == "bson.objectid" and classname == "ObjectId":
                return bson.objectid.ObjectId(d["oid"])

            return {
                self.process_decoded(k): self.process_decoded(v)
                for k, v in d.items()
            }

        if isinstance(d, list):
            return [self.process_decoded(x) for x in d]

        return d

    def decode(self, s):
        """
        Overrides decode from JSONDecoder.

        :param s: string
        :return: Object.
        """
        d = json.JSONDecoder.decode(self, s)
        return self.process_decoded(d)


class MSONError(Exception):
    """
    Exception class for serialization errors.
    """


def jsanitize(obj, strict=False, allow_bson=False):
    """
    This method cleans an input json-like object, either a list or a dict or
    some sequence, nested or otherwise, by converting all non-string
    dictionary keys (such as int and float) to strings, and also recursively
    encodes all objects using Monty's as_dict() protocol.

    Args:
        obj: input json-like object.
        strict (bool): This parameters sets the behavior when jsanitize
            encounters an object it does not understand. If strict is True,
            jsanitize will try to get the as_dict() attribute of the object. If
            no such attribute is found, an attribute error will be thrown. If
            strict is False, jsanitize will simply call str(object) to convert
            the object to a string representation.
        allow_bson (bool): This parameters sets the behavior when jsanitize
            encounters an bson supported type such as objectid and datetime. If
            True, such bson types will be ignored, allowing for proper
            insertion into MongoDb databases.

    Returns:
        Sanitized dict that can be json serialized.
    """
    if allow_bson and (isinstance(obj, (datetime.datetime, bytes)) or
                       (bson is not None
                        and isinstance(obj, bson.objectid.ObjectId))):
        return obj
    if isinstance(obj, (list, tuple)):
        return [
            jsanitize(i, strict=strict, allow_bson=allow_bson) for i in obj
        ]
    if np is not None and isinstance(obj, np.ndarray):
        return [
            jsanitize(i, strict=strict, allow_bson=allow_bson)
            for i in obj.tolist()
        ]
    if isinstance(obj, dict):
        return {
            k.__str__(): jsanitize(v, strict=strict, allow_bson=allow_bson)
            for k, v in obj.items()
        }
    if isinstance(obj, (int, float)):
        return obj
    if obj is None:
        return None

    if not strict:
        return obj.__str__()

    if isinstance(obj, str):
        return obj.__str__()

    return jsanitize(obj.as_dict(), strict=strict, allow_bson=allow_bson)
