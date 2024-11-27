"""
Useful collection classes:
    - tree: A recursive `defaultdict` for creating nested dictionaries
        with default values.
    - ControlledDict: A base dict class with configurable mutability.
    - frozendict: An immutable dictionary.
    - Namespace: A dict doesn't allow changing values, but could
        add new keys,
    - AttrDict: A dict whose values could be access as `dct.key`.
    - FrozenAttrDict: An immutable version of `AttrDict`.
    - MongoDict: A dict-like object whose values are nested dicts
        could be accessed as attributes.
"""

from __future__ import annotations

import collections
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, ClassVar, Iterable

    from typing_extensions import Self


def tree() -> collections.defaultdict:
    """
    A tree object, which is effectively a recursive defaultdict that
    adds tree as members.

    Usage:
        x = tree()
        x["a"]["b"]["c"] = 1

    Returns:
        A tree.
    """
    return collections.defaultdict(tree)


class ControlledDict(collections.UserDict, ABC):
    """
    A base dictionary class with configurable mutability.

    Attributes:
        allow_add (bool): Whether new keys can be added.
        allow_del (bool): Whether existing keys can be deleted.
        allow_update (bool): Whether existing keys can be updated.

    Configurable Operations:
        This class allows controlling the following dictionary operations (refer to
        https://docs.python.org/3.13/library/stdtypes.html#mapping-types-dict for details):

        - Adding or updating items:
            - setter method: `__setitem__`
            - `setdefault`
            - `update`

        - Deleting items:
            - `del dict[key]`
            - `pop(key)`
            - `popitem`
            - `clear()`
    """

    allow_add: ClassVar[bool] = True
    allow_del: ClassVar[bool] = True
    allow_update: ClassVar[bool] = True

    def __init__(self, *args, **kwargs):
        """Temporarily allow all add/update during initialization."""
        original_allow_add = self.allow_add
        original_allow_update = self.allow_update
        try:
            self.allow_add = True
            self.allow_update = True
            super().__init__(*args, **kwargs)
        finally:
            self.allow_add = original_allow_add
            self.allow_update = original_allow_update

    # TODO: extract checkers

    # Overriding add/update operations
    def __setitem__(self, key, value):
        """Forbid adding or updating keys based on allow_add and allow_update."""
        if key not in self.data and not self.allow_add:
            raise TypeError(
                f"Cannot add new key {key!r}, because allow_add is set to False."
            )
        elif key in self.data and not self.allow_update:
            raise TypeError(
                f"Cannot update key {key!r}, because allow_update is set to False."
            )

        super().__setitem__(key, value)

    def update(self, *args, **kwargs):
        """Forbid adding or updating keys based on allow_add and allow_update."""
        for key in dict(*args, **kwargs):
            if key not in self.data and not self.allow_add:
                raise TypeError(
                    f"Cannot add new key {key!r} using update, because allow_add is set to False."
                )
            elif key in self.data and not self.allow_update:
                raise TypeError(
                    f"Cannot update key {key!r} using update, because allow_update is set to False."
                )

        super().update(*args, **kwargs)

    def setdefault(self, key, default=None):
        """Forbid adding or updating keys based on allow_add and allow_update.

        Note: if not allow_update, this method would NOT check whether the
            new default value is the same as current value for efficiency.
        """
        if key not in self.data:
            if not self.allow_add:
                raise TypeError(
                    f"Cannot add new key using setdefault: {key!r}, because allow_add is set to False."
                )
        elif not self.allow_update:
            raise TypeError(
                f"Cannot update key using setdefault: {key!r}, because allow_update is set to False."
            )

        return super().setdefault(key, default)

    # Overriding delete operations
    def __delitem__(self, key):
        """Forbid deleting keys when self.allow_del is False."""
        if not self.allow_del:
            raise TypeError(f"Cannot delete key {key!r}, because delete is disabled.")
        super().__delitem__(key)

    def pop(self, key, *args):
        """Forbid popping keys when self.allow_del is False."""
        if not self.allow_del:
            raise TypeError(f"Cannot pop key {key!r}, because delete is disabled.")
        return super().pop(key, *args)

    def popitem(self):
        """Forbid popping the last item when self.allow_del is False."""
        if not self.allow_del:
            raise TypeError("Cannot pop item, because delete is disabled.")
        return super().popitem()

    def clear(self):
        """Forbid clearing the dictionary when self.allow_del is False."""
        if not self.allow_del:
            raise TypeError("Cannot clear dictionary, because delete is disabled.")
        super().clear()


class frozendict(ControlledDict):
    """
    A dictionary that does not permit changes. The naming
    violates PEP 8 to be consistent with the built-in `frozenset` naming.
    """

    allow_add: ClassVar[bool] = False
    allow_del: ClassVar[bool] = False
    allow_update: ClassVar[bool] = False


class Namespace(dict):  # TODO: this name is a bit confusing, deprecate it?
    """A dictionary that does not permit changing its values."""

    def __init__(self, *args, **kwargs) -> None:
        """
        Args:
            args: Passthrough arguments for standard dict.
            kwargs: Passthrough keyword arguments for standard dict.
        """
        self.update(*args, **kwargs)

    def __setitem__(self, key: Any, val: Any) -> None:
        if key in self:
            raise TypeError(f"Cannot overwrite existing key: {key!s}")

        dict.__setitem__(self, key, val)

    def update(self, *args, **kwargs) -> None:
        """
        Args:
            args: Passthrough arguments for standard dict.
            kwargs: Passthrough keyword arguments for standard dict.
        """
        for k, v in dict(*args, **kwargs).items():
            self[k] = v


class AttrDict(dict):
    """
    Allows to access values as dct.key in addition
    to the traditional way dct["key"]

    Examples:
        >>> dct = AttrDict(foo=1, bar=2)
        >>> assert dct["foo"] is dct.foo
        >>> dct.bar = "hello"
        >>> assert dct.bar == "hello"
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Args:
            args: Passthrough arguments for standard dict.
            kwargs: Passthrough keyword arguments for standard dict.
        """
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def copy(self) -> Self:
        """
        Returns:
            Copy of AttrDict
        """
        newd = super().copy()
        return self.__class__(**newd)


class FrozenAttrDict(frozendict):
    """
    A dictionary that:
        - Does not permit changes.
        - Allows to access values as dct.key in addition
          to the traditional way dct["key"]
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Args:
            args: Passthrough arguments for standard dict.
            kwargs: Passthrough keyword arguments for standard dict.
        """
        super().__init__(*args, **kwargs)

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            try:
                return self[name]
            except KeyError as exc:
                raise AttributeError(str(exc))

    def __setattr__(self, name: str, value: Any) -> None:
        raise TypeError(
            f"You cannot modify attribute {name} of {self.__class__.__name__}"
        )


class MongoDict:
    """
    This dict-like object allows one to access the entries in a nested dict as
    attributes.
    Entries (attributes) cannot be modified. It also provides Ipython tab
    completion hence this object is particularly useful if you need to analyze
    a nested dict interactively (e.g. documents extracted from a MongoDB
    database).

    >>> m_dct = MongoDict({"a": {"b": 1}, "x": 2})
    >>> assert m_dct.a.b == 1 and m_dct.x == 2
    >>> assert "a" in m_dct and "b" in m_dct.a
    >>> m_dct["a"]
    {"b": 1}

    Notes:
        Cannot inherit from ABC collections.Mapping because otherwise
        dict.keys and dict.items will pollute the namespace.
        e.g MongoDict({"keys": 1}).keys would be the ABC dict method.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Args:
            args: Passthrough arguments for standard dict.
            kwargs: Passthrough keyword arguments for standard dict.
        """
        self.__dict__["_mongo_dict_"] = dict(*args, **kwargs)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(self._mongo_dict_)

    def __setattr__(self, name: str, value: Any) -> None:
        raise NotImplementedError(
            f"You cannot modify attribute {name} of {self.__class__.__name__}"
        )

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            try:
                a = self._mongo_dict_[name]
                if isinstance(a, collections.abc.Mapping):
                    a = self.__class__(a)
                return a
            except Exception as exc:
                raise AttributeError(str(exc))

    def __getitem__(self, slice_) -> Any:
        return self._mongo_dict_.__getitem__(slice_)

    def __iter__(self) -> Iterable:
        return iter(self._mongo_dict_)

    def __len__(self) -> int:
        return len(self._mongo_dict_)

    def __dir__(self) -> list:
        """
        For Ipython tab completion.
        See http://ipython.org/ipython-doc/dev/config/integrating.html
        """
        return sorted(k for k in self._mongo_dict_ if not callable(k))


def dict2namedtuple(*args, **kwargs) -> tuple:
    """
    Helper function to create a `namedtuple` from a dictionary.

    Examples:
        >>> tpl = dict2namedtuple(foo=1, bar="hello")
        >>> assert tpl.foo == 1 and tpl.bar == "hello"

        >>> tpl = dict2namedtuple([("foo", 1), ("bar", "hello")])
        >>> assert tpl[0] is tpl.foo and t[1] is tpl.bar

    Warnings:
        - The order of the items in the namedtuple is not deterministic if
          `kwargs` are used. namedtuples, however, should always be accessed
          by attribute hence this behaviour should not be a serious problem.

        - Don't use this function in code where memory and performance are
          crucial, since a dict is needed to instantiate the tuple!
    """
    dct = collections.OrderedDict(*args)
    dct.update(**kwargs)
    return collections.namedtuple(
        typename="dict2namedtuple", field_names=list(dct.keys())
    )(**dct)
