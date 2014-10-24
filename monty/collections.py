from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


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
        >> d = AttrDict(foo=1, bar=2)
        >> d["foo"] == d.foo
        True
        >> d.bar = "hello"
        >> d.bar
        'hello'
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
        raise KeyError("You cannot modify attribute %s of %s" % (name, self.__class__.__name__))

