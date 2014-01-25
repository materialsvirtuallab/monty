__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


class frozendict(dict):
    """
    A dictionary that does not permit to redefine its keys. The naming
    violates PEP8 to be consistent with standard Python's "frozenset" naming.
    """
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

    def __setitem__(self, key, val):
        raise KeyError("Cannot overwrite existing key: %s" % str(key))
