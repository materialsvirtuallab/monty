---
layout: default
title: monty.fractions.md
nav_exclude: true
---

# monty.fractions module

Math functions.

## monty.fractions.gcd(\*numbers)

Returns the greatest common divisor for a sequence of numbers.

* **Parameters**
  **\*numbers** – Sequence of numbers.
* **Returns**
  (int) Greatest common divisor of numbers.

## monty.fractions.gcd_float(numbers, tol=1e-08)

Returns the greatest common divisor for a sequence of numbers.
Uses a numerical tolerance, so can be used on floats

* **Parameters**
  * **numbers** – Sequence of numbers.
  * **tol** – Numerical tolerance
* **Returns**
  (int) Greatest common divisor of numbers.

## monty.fractions.lcm(\*numbers)

Return lowest common multiple of a sequence of numbers.

* **Parameters**
  **\*numbers** – Sequence of numbers.
* **Returns**
  (int) Lowest common multiple of numbers.