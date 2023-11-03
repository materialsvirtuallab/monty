---
layout: default
title: monty.logging.md
nav_exclude: true
---

# monty.logging module

Logging tools

## monty.logging.enable_logging(main)

This decorator is used to decorate main functions.
It adds the initialization of the logger and an argument parser that allows
one to select the loglevel.
Useful if we are writing simple main functions that call libraries where
the logging module is used

* **Parameters**
  **main** – main function.

## monty.logging.logged(level=10)

Useful logging decorator. If a method is logged, the beginning and end of
the method call will be logged at a pre-specified level.

* **Parameters**
  **level** – Level to log method at. Defaults to DEBUG.