---
layout: default
title: monty.pprint.md
nav_exclude: true
---

# monty.pprint module

Pretty printing functions.


### _class_ monty.pprint.DisplayEcoder(\*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)
Bases: `JSONEncoder`

Help convert dicts and objects to a format that can be displayed in notebooks

Constructor for JSONEncoder, with sensible defaults.

If skipkeys is false, then it is a TypeError to attempt
encoding of keys that are not str, int, float or None.  If
skipkeys is True, such items are simply skipped.

If ensure_ascii is true, the output is guaranteed to be str
objects with all incoming non-ASCII characters escaped.  If
ensure_ascii is false, the output can contain non-ASCII characters.

If check_circular is true, then lists, dicts, and custom encoded
objects will be checked for circular references during encoding to
prevent an infinite recursion (which would cause an RecursionError).
Otherwise, no such check takes place.

If allow_nan is true, then NaN, Infinity, and -Infinity will be
encoded as such.  This behavior is not JSON specification compliant,
but is consistent with most JavaScript based encoders and decoders.
Otherwise, it will be a ValueError to encode such floats.

If sort_keys is true, then the output of dictionaries will be
sorted by key; this is useful for regression tests to ensure
that JSON serializations can be compared on a day-to-day basis.

If indent is a non-negative integer, then JSON array
elements and object members will be pretty-printed with that
indent level.  An indent level of 0 will only insert newlines.
None is the most compact representation.

If specified, separators should be an (item_separator, key_separator)
tuple.  The default is (’, ‘, ‘: ‘) if *indent* is `None` and
(‘,’, ‘: ‘) otherwise.  To get the most compact JSON representation,
you should specify (‘,’, ‘:’) to eliminate whitespace.

If specified, default is a function that gets called for objects
that can’t otherwise be serialized.  It should return a JSON encodable
version of the object or raise a `TypeError`.


#### default(o)
Try diffent ways of converting the present object for displaying


### monty.pprint.draw_tree(node, child_iter=<function <lambda>>, text_str=<function <lambda>>)

* **Parameters**


    * **node** – the root of the tree to be drawn,


    * **child_iter** – function that when called with a node, returns an iterable
    over all its children


    * **text_str** – turns a node into the text to be displayed in the tree.


The default implementations of these two arguments retrieve the children
by accessing node.children and simply use str(node) to convert a node to a
string. The resulting tree is drawn into a buffer and returned as a string.

Based on [https://pypi.python.org/pypi/asciitree/](https://pypi.python.org/pypi/asciitree/)


### monty.pprint.pprint_json(data)
Display a tree-like object in a jupyter notebook.
Allows for collapsable interactive interaction with data.


* **Parameters**

    **data** – a dictionary or object


Based on:
[https://gist.github.com/jmmshn/d37d5a1be80a6da11f901675f195ca22](https://gist.github.com/jmmshn/d37d5a1be80a6da11f901675f195ca22)


### monty.pprint.pprint_table(table, out=<_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>, rstrip=False)
Prints out a table of data, padded for alignment
Each row must have the same number of columns.


* **Parameters**


    * **table** – The table to print. A list of lists.


    * **out** – Output stream (file-like object)


    * **rstrip** – if True, trailing withespaces are removed from the entries.