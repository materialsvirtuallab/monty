---
layout: default
title: monty.bisect.md
nav_exclude: true
---

# monty.bisect module

Additional bisect functions. Taken from
[https://docs.python.org/2/library/bisect.html](https://docs.python.org/2/library/bisect.html)
The above bisect() functions are useful for finding insertion points but can be
tricky or awkward to use for common searching tasks.
The functions show how to transform them into the standard lookups for sorted
lists.

## monty.bisect.find_ge(a, x)

Find leftmost item greater than or equal to x.

## monty.bisect.find_gt(a, x)

Find leftmost value greater than x.

## monty.bisect.find_le(a, x)

Find rightmost value less than or equal to x.

## monty.bisect.find_lt(a, x)

Find rightmost value less than x.

## monty.bisect.index(a, x, atol=None)

Locate the leftmost value exactly equal to x.