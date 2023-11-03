---
layout: default
title: monty.itertools.md
nav_exclude: true
---

# monty.itertools module

Additional tools for iteration.

## monty.itertools.chunks(items, n)

Yield successive n-sized chunks from a list-like object.

```python
>>> import pprint
>>> pprint.pprint(list(chunks(range(1, 25), 10)))
[(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
 (11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
 (21, 22, 23, 24)]
```

## monty.itertools.ilotri(items, diago=True, with_inds=False)

A generator that yields the lower triangle of the matrix (items x items)

* **Parameters**
  * **items** – Iterable object with elements [e0, e1, …]
  * **diago** – False if diagonal matrix elements should be excluded
  * **with_inds** – If True, (i,j) (e_i, e_j) is returned else (e_i, e_j)

```python
>>> for (ij, mate) in ilotri([0,1], with_inds=True):
...     print("ij:", ij, "mate:", mate)
ij: (0, 0) mate: (0, 0)
ij: (1, 0) mate: (1, 0)
ij: (1, 1) mate: (1, 1)
```

## monty.itertools.iterator_from_slice(s)

Constructs an iterator given a slice object s.

**NOTE**: The function returns an infinite iterator if s.stop is None

## monty.itertools.iuptri(items, diago=True, with_inds=False)

A generator that yields the upper triangle of the matrix (items x items)

* **Parameters**
  * **items** – Iterable object with elements [e0, e1, …]
  * **diago** – False if diagonal matrix elements should be excluded
  * **with_inds** – If True, (i,j) (e_i, e_j) is returned else (e_i, e_j)

```python
>>> for (ij, mate) in iuptri([0,1], with_inds=True):
...     print("ij:", ij, "mate:", mate)
ij: (0, 0) mate: (0, 0)
ij: (0, 1) mate: (0, 1)
ij: (1, 1) mate: (1, 1)
```