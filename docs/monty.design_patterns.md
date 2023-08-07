---
layout: default
title: monty.design_patterns.md
nav_exclude: true
---

# monty.design_patterns module

Some common design patterns such as singleton and cached classes.


### _class_ monty.design_patterns.NullFile()
Bases: `object`

A file object that is associated to /dev/null.

no-op


### _class_ monty.design_patterns.NullStream()
Bases: `object`

A fake stream with a no-op write..


#### write()
Does nothing…
:param args:


### monty.design_patterns.cached_class(klass)
Decorator to cache class instances by constructor arguments.
This results in a class that behaves like a singleton for each
set of constructor arguments, ensuring efficiency.

Note that this should be used for *immutable classes only*.  Having
a cached mutable class makes very little sense.  For efficiency,
avoid using this decorator for situations where there are many
constructor arguments permutations.

The keywords argument dictionary is converted to a tuple because
dicts are mutable; keywords themselves are strings and
so are always hashable, but if any arguments (keyword
or positional) are non-hashable, that set of arguments
is not cached.


### monty.design_patterns.singleton(cls)
This decorator can be used to create a singleton out of a class.

Usage:

```default
@singleton
class MySingleton():

    def __init__():
        pass
```