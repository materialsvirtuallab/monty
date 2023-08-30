---
layout: default
title: monty.fnmatch.md
nav_exclude: true
---

# monty.fnmatch module

This module provides support for Unix shell-style wildcards


### _class_ monty.fnmatch.WildCard(wildcard, sep='|')
Bases: `object`

This object provides an easy-to-use interface for filename matching with
shell patterns (fnmatch).

```python
>>> w = WildCard("*.nc|*.pdf")
>>> w.filter(["foo.nc", "bar.pdf", "hello.txt"])
['foo.nc', 'bar.pdf']
```

```python
>>> w.filter("foo.nc")
['foo.nc']
```

Initializes a WildCard.


* **Parameters**


    * **wildcard** (*str*) – String of tokens separated by sep. Each token
    represents a pattern.


    * **sep** (*str*) – Separator for shell patterns.



#### filter(names)
Returns a list with the names matching the pattern.


#### match(name)
Returns True if name matches one of the patterns.