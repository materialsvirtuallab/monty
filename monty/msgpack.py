"""
msgpack serialization and deserialization utilities. Right now, this is a stub
using monty.json encoder and decoders. The naming is just for clearer usage with
msgpack's default and object_hook naming.
"""

from __future__ import absolute_import, unicode_literals

from monty.json import MontyEncoder, MontyDecoder


def default(obj):
    """
    For use with msgpack.packb(obj, default=default). Supports Monty's as_dict
    protocol, numpy arrays and datetime.
    """
    return MontyEncoder().default(obj)


def object_hook(d):
    """
    For use with msgpack.unpackb(dict, object_hook=object_hook.).  Supports
    Monty's as_dict protocol, numpy arrays and datetime.
    """
    return MontyDecoder().process_decoded(d)