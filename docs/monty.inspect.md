---
layout: default
title: monty.inspect.md
nav_exclude: true
---

# monty.inspect module

Useful additional functions to help get information about live objects


### monty.inspect.all_subclasses(cls)
Given a class cls, this recursive function returns a list with
all subclasses, subclasses of subclasses, and so on.


### monty.inspect.caller_name(skip=2)
Get a name of a caller in the format module.class.method

skip specifies how many levels of stack to skip while getting caller
name. skip=1 means “who calls me”, skip=2 “who calls my caller” etc.

An empty string is returned if skipped levels exceed stack height

Taken from:

> [https://gist.github.com/techtonik/2151727](https://gist.github.com/techtonik/2151727)

Public Domain, i.e. feel free to copy/paste


### monty.inspect.find_top_pyfile()
This function inspects the Cpython frame to find the path of the script.


### monty.inspect.initializer(func)
Automatically assigns the parameters.
[http://stackoverflow.com/questions/1389180/python-automatically-initialize](http://stackoverflow.com/questions/1389180/python-automatically-initialize)
-instance-variables

```python
>>> class process:
...     @initializer
...     def __init__(self, cmd, reachable=False, user='root'):
...         pass
>>> p = process('halt', True)
>>> p.cmd, p.reachable, p.user
('halt', True, 'root')
```