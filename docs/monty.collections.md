---
layout: default
title: monty.collections.md
nav_exclude: true
---

# monty.collections module

Useful collection classes, e.g., tree, frozendict, etc.

## *class* monty.collections.AttrDict(\*args, \*\*kwargs)

Bases: `dict`

Allows to access dict keys as obj.foo in addition
to the traditional way obj[‘foo’]”

## Example

```python
>>> d = AttrDict(foo=1, bar=2)
>>> assert d["foo"] == d.foo
>>> d.bar = "hello"
>>> assert d.bar == "hello"
```

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

### copy()

* **Returns**
  Copy of AttrDict

## *class* monty.collections.FrozenAttrDict(\*args, \*\*kwargs)

Bases: `frozendict`

A dictionary that:

```none
* does not permit changes.


* Allows to access dict keys as obj.foo in addition
to the traditional way obj[‘foo’]
```

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

## *class* monty.collections.MongoDict(\*args, \*\*kwargs)

Bases: `object`

This dict-like object allows one to access the entries in a nested dict as
attributes.
Entries (attributes) cannot be modified. It also provides Ipython tab
completion hence this object is particularly useful if you need to analyze
a nested dict interactively (e.g. documents extracted from a MongoDB
database).

```python
>>> m = MongoDict({'a': {'b': 1}, 'x': 2})
>>> assert m.a.b == 1 and m.x == 2
>>> assert "a" in m and "b" in m.a
>>> m["a"]
{'b': 1}
```

**NOTE**: Cannot inherit from ABC collections.Mapping because otherwise
dict.keys and dict.items will pollute the namespace.
e.g MongoDict({“keys”: 1}).keys would be the ABC dict method.

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

## *class* monty.collections.Namespace(\*args, \*\*kwargs)

Bases: `dict`

A dictionary that does not permit to redefine its keys.

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

### update(\*args, \*\*kwargs)

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

## monty.collections.dict2namedtuple(\*args, \*\*kwargs)

Helper function to create a `namedtuple` from a dictionary.

## Example

```python
>>> t = dict2namedtuple(foo=1, bar="hello")
>>> assert t.foo == 1 and t.bar == "hello"
```

```python
>>> t = dict2namedtuple([("foo", 1), ("bar", "hello")])
>>> assert t[0] == t.foo and t[1] == t.bar
```

**WARNING**:

* The order of the items in the namedtuple is not deterministic if
  kwargs are used.
  namedtuples, however, should always be accessed by attribute hence
  this behaviour should not represent a serious problem.
* Don’t use this function in code in which memory and performance are
  crucial since a dict is needed to instantiate the tuple!

## *class* monty.collections.frozendict(\*args, \*\*kwargs)

Bases: `dict`

A dictionary that does not permit changes. The naming
violates PEP8 to be consistent with standard Python’s “frozenset” naming.

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

### update(\*args, \*\*kwargs)

* **Parameters**
  * **args** – Passthrough arguments for standard dict.
  * **kwargs** – Passthrough keyword arguments for standard dict.

## monty.collections.tree()

A tree object, which is effectively a recursive defaultdict that
adds tree as members.

Usage:

```none
x = tree()
x[‘a’][‘b’][‘c’] = 1
```

* **Returns**
  A tree.