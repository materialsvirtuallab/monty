.. monty documentation master file, created by
   sphinx-quickstart on Tue Nov 15 00:13:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Monty - The Missing Complement to Python
========================================

.. image:: https://travis-ci.org/materialsvirtuallab/monty.png?branch=master
.. image:: https://coveralls.io/repos/github/materialsvirtuallab/monty/badge.svg?branch=master

Monty is the missing complement to Python. Monty implements supplementary
useful functions for Python that are not part of the standard library.
Examples include useful utilities like transparent support for zipped files,
useful design patterns such as singleton and cached_class, and many more.

Why Monty?
==========

Python is a wonderful programming language and comes with "batteries
included". However, even Python has missing functionality and/or quirks that
make it more difficult to do many simple tasks. In the process of
creating several large scientific frameworks based on Python,
my co-developers and I have found that it is often useful to create
reusable utility  functions to supplement the Python standard library. Our
forays in various developer sites and forums also found that many developers
are looking for solutions to the same problems.

Monty is created to serve as a complement to the Python standard library. It
provides suite of tools to solve many common problems, and hopefully,
be a resource to collect the best solutions.

Compatibility
-------------

Monty is tested to work on Python 2.7 and 3.x.

Latest Change Log
=================

v0.9.0
------
1. Improved default as and from_dict.

v0.8.5
------
1. Minor bug fixes.

v0.8.4
------
1. Support for bson fields in jsanitize.

v0.8.2
------
1. Fasetr gzip.

v0.8.1
------
1. Update gcd for deprecated fractions.gcd in py >= 3.5. Try math.gcd by default first.

:doc:`Older versions </changelog>`

Installing monty
================

The easiest way to install monty on any system is to use easy_install or
pip, as follows::

    easy_install monty

or::

    pip install monty

Usage
=====

Unlike most other modules, the organization of Monty mirrors that of the
standard Python library where possible. This style is adopted so that that
it is almost always obvious where a particular method or function
will reside. There are two recommended ways of using Monty.

Method 1: Import the monty root::

    import monty as mt
    with mt.io.zopen("src.gz") as f:
        data = f.read()
    with mt.io.zopen("dest.bz2", "wb") as f:
        f.write(data)

Method 2: Import specific functions as needed::

    from monty.io import zopen
    with zopen("file.gz") as f:
        data = f.read()
    with zopen("dest.bz2", "wb") as f:
        f.write(data)

The above is an example of how Monty supplements the standard Python library.
The standard library contains functions for dealing with gzipped and bzip2
files. What Monty adds is a layer of abstraction that allows the type of
compression (or no compression) to be determined from the filename and the
appropriate standard library function is chosen to open the files. All the
typical args and kwargs of "open" are supported. The syntax "zopen" mirrors
standard Unix's zless/zgrep commands.

Below are some further examples of Monty's features::

    from monty.design_patterns import singleton, cached_class

    # The singleton design pattern

    @singleton
    class A():
        pass

    # Note that cached classes must be new style, i.e. inherits object in
    # Python 2.7. A cached class is one which has one unique instance per
    # set of args and kwargs.

    @cached_class
    class B(object):

        def __init__(self, b):
            self.b = b

    # Highly efficient of reading of lines from back of file.

    from monty.io import zopen, reverse_readline
    with zopen("myfile") as f:
        for line in reverse_readline(f):
            print line

    # A frozen dict (Immutable dict)

    from monty.collections import frozendict
    d = frozendict(a=1)

API docs
--------

The API docs are given below. The docs for most classes or methods are clear
enough for usage. Where there is somewhat greater subtlety in the usage,
examples are provided.

.. toctree::

   monty

Contributing
============

Contributions to Monty are always welcome. Feel free to visit the `Monty
Github repo <https://github.com/materialsvirtuallab/monty>`_ to fork the
repo or to submit Issues.

License
=======

Monty is released under the MIT License. The terms of the license are as
follows:

.. literalinclude:: ../LICENSE.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
