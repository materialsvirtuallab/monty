monty
=====

Monty implements supplementary useful functions for Python that are
not part of the standard library. Examples include useful utilities like
transparent support for zipped files, useful design patterns such as
singleton and cached_class, and many more.

The organization of Monty follows the standard Python library where possible
so that it is almost always obvious where a particular method or function
will reside. Monty will also always be pure Python (without the need for
extensions), and have minimal *required dependencies* (some complements to
non-standard library components such as numpy may require the non-standard
library, but will be completely optional).
