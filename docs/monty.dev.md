---
layout: default
title: monty.dev.md
nav_exclude: true
---

# monty.dev module

This module implements several useful functions and decorators that can be
particularly useful for developers. E.g., deprecating methods / classes, etc.

## monty.dev.deprecated(replacement=None, message=None, category=<class ‘FutureWarning’>)

Decorator to mark classes or functions as deprecated,
with a possible replacement.

* **Parameters**
  * **replacement** (*callable*) – A replacement class or method.
  * **message** (*str*) – A warning message to be displayed.
  * **category** (*Warning*) – Choose the category of the warning to issue. Defaults
    to FutureWarning. Another choice can be DeprecationWarning. NOte that
    FutureWarning is meant for end users and is always shown unless silenced.
    DeprecationWarning is meant for developers and is never shown unless
    python is run in developmental mode or the filter is changed. Make
    the choice accordingly.
* **Returns**
  Original function, but with a warning to use the updated class.

## monty.dev.install_excepthook(hook_type=’color’, \*\*kwargs)

This function replaces the original python traceback with an improved
version from Ipython. Use color for colourful traceback formatting,
verbose for Ka-Ping Yee’s “cgitb.py” version kwargs are the keyword
arguments passed to the constructor. See IPython.core.ultratb.py for more
info.

* **Returns**
  0 if hook is installed successfully.

## *class* monty.dev.requires(condition, message)

Bases: `object`

Decorator to mark classes or functions as requiring a specified condition
to be true. This can be used to present useful error messages for
optional dependencies. For example, decorating the following code will
check if scipy is present and if not, a runtime error will be raised if
someone attempts to call the use_scipy function:

```default
try:
    import scipy
except ImportError:
    scipy = None

@requires(scipy is not None, "scipy is not present.")
def use_scipy():
    print(scipy.majver)
```

* **Parameters**
  * **condition** – Condition necessary to use the class or function.
  * **message** – A message to be displayed if the condition is not True.
  * **condition** – A expression returning a bool.
  * **message** – Message to display if condition is False.