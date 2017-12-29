# coding: utf-8
from __future__ import absolute_import, print_function, unicode_literals, \
    division

import collections

__author__ = 'Shyue Ping Ong'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


def tree():
    """
    A tree object, which is effectively a recursive defaultdict that
    adds tree as members.

    Usage:
        x = tree()
        x['a']['b']['c'] = 1

    Returns:
        A tree.
    """
    return collections.defaultdict(tree)


def as_set(obj):
    """
    Convert obj into a set, returns None if obj is None.

    >>> assert as_set(None) is None and as_set(1) == set([1]) and as_set(range(1,3)) == set([1, 2])
    """
    if obj is None or isinstance(obj, collections.Set):
        return obj

    if not isinstance(obj, collections.Iterable):
        return set((obj,))
    else:
        return set(obj)


class frozendict(dict):
    """
    A dictionary that does not permit changes. The naming
    violates PEP8 to be consistent with standard Python's "frozenset" naming.
    """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, val):
        raise KeyError("Cannot overwrite existing key: %s" % str(key))

    def update(self, *args, **kwargs):
        raise KeyError("Cannot update a %s" % self.__class__.__name__)


class Namespace(dict):
    """A dictionary that does not permit to redefine its keys."""

    def __init__(self, *args, **kwargs):
        self.update(*args, **kwargs)

    def __setitem__(self, key, val):
        if key in self:
            raise KeyError("Cannot overwrite existent key: %s" % str(key))

        dict.__setitem__(self, key, val)

    def update(self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class AttrDict(dict):
    """
    Allows to access dict keys as obj.foo in addition
    to the traditional way obj['foo']"

    Example:
        >>> d = AttrDict(foo=1, bar=2)
        >>> assert d["foo"] == d.foo
        >>> d.bar = "hello"
        >>> assert d.bar == "hello"
    """

    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def copy(self):
        newd = super(AttrDict, self).copy()
        return self.__class__(**newd)


class FrozenAttrDict(frozendict):
    """
    A dictionary that:
        * does not permit changes. 
        * Allows to access dict keys as obj.foo in addition
          to the traditional way obj['foo']
    """

    def __init__(self, *args, **kwargs):
        super(FrozenAttrDict, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        try:
            return super(FrozenAttrDict, self).__getattribute__(name)
        except AttributeError:
            try:
                return self[name]
            except KeyError as exc:
                raise AttributeError(str(exc))

    def __setattr__(self, name, value):
        raise KeyError("You cannot modify attribute %s of %s" % (
            name, self.__class__.__name__))


class MongoDict(object):
    """
    This dict-like object allows one to access the entries in a nested dict as attributes. 
    Entries (attributes) cannot be modified. It also provides Ipython tab completion hence this object 
    is particularly useful if you need to analyze a nested dict interactively (e.g. documents
    extracted from a MongoDB database).

    >>> m = MongoDict({'a': {'b': 1}, 'x': 2}) 
    >>> assert m.a.b == 1 and m.x == 2
    >>> assert "a" in m and "b" in m.a
    >>> m["a"]
    {'b': 1}

    .. note:: 

        Cannot inherit from ABC collections.Mapping because otherwise 
        dict.keys and dict.items will pollute the namespace.
        e.g MongoDict({"keys": 1}).keys would be the ABC dict method.
    """

    def __init__(self, *args, **kwargs):
        self.__dict__["_mongo_dict_"] = dict(*args, **kwargs)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str(self._mongo_dict_)

    def __setattr__(self, name, value):
        raise NotImplementedError("You cannot modify attribute %s of %s" % (
            name, self.__class__.__name__))

    def __getattribute__(self, name):
        try:
            return super(MongoDict, self).__getattribute__(name)
        except:
            # raise
            try:
                a = self._mongo_dict_[name]
                if isinstance(a, collections.Mapping):
                    a = self.__class__(a)
                return a
            except Exception as exc:
                raise AttributeError(str(exc))

    def __getitem__(self, slice_):
        return self._mongo_dict_.__getitem__(slice_)

    def __iter__(self):
        return iter(self._mongo_dict_)

    def __len__(self):
        return len(self._mongo_dict_)

    def __dir__(self):
        """
        For Ipython tab completion.
        See http://ipython.org/ipython-doc/dev/config/integrating.html
        """
        return sorted(list(k for k in self._mongo_dict_ if not callable(k)))


def dict2namedtuple(*args, **kwargs):
    """
    Helper function to create a :class:`namedtuple` from a dictionary.

    Example:

        >>> t = dict2namedtuple(foo=1, bar="hello")
        >>> assert t.foo == 1 and t.bar == "hello"

        >>> t = dict2namedtuple([("foo", 1), ("bar", "hello")])
        >>> assert t[0] == t.foo and t[1] == t.bar

    .. warning::

        - The order of the items in the namedtuple is not deterministic if
          kwargs are used.
          namedtuples, however, should always be accessed by attribute hence 
          this behaviour should not represent a serious problem.

        - Don't use this function in code in which memory and performance are
          crucial since a dict is needed to instantiate the tuple!
    """
    d = collections.OrderedDict(*args)
    d.update(**kwargs)
    return collections.namedtuple(typename="dict2namedtuple",
                                  field_names=list(d.keys()))(**d)
