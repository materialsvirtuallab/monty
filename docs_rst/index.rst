.. monty documentation master file, created by
   sphinx-quickstart on Tue Nov 15 00:13:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Monty: Python Made Even Easier
==============================

.. image:: https://travis-ci.org/materialsvirtuallab/monty.png?branch=master
.. image:: https://coveralls.io/repos/github/materialsvirtuallab/monty/badge.svg?branch=master
.. image:: https://anaconda.org/conda-forge/monty/badges/downloads.svg

Monty is the missing complement to Python. Monty implements supplementary
useful functions for Python that are not part of the standard library.
Examples include useful utilities like transparent support for zipped files,
useful design patterns such as singleton and cached_class, and many more.

Python is a great programming language and comes with "batteries
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

Monty currently supports Python 2.7-3.x, but please note that with effect from
v3.x, which will be released in Jan 2020, we will completely abandon Py2.7
support, in line with most other Python packages.

Change Log
==========

v3.0.1
------
1. Bug fixes for Windows.

v3.0.0
------
1. Py3 only version.

v2.0.7
------
1. MSONable now supports Enum types. (@mkhorton)

:doc:`Older versions </changelog>`

Installation
============

Standard pip install::

    pip install monty

Usage
=====

Unlike most other modules, the organization of Monty mirrors that of the
standard Python library where possible. This style is adopted so that that
it is almost always obvious where a particular method or function
will reside. There are two recommended ways of using Monty.

Method 1: Import the monty root::

    import monty as mty
    with mty.io.zopen("src.gz") as f:
        data = f.read()
    with mty.io.zopen("dest.bz2", "wb") as f:
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
            print(line)

    # A frozen dict (Immutable dict)

    from monty.collections import frozendict
    d = frozendict(a=1)

    # A Fabric-inspired cd context, that allows one to change directory to
    # execute code and transparently changes back to the current working
    # directory

    from monty.os import cd

    with cd("/path/to/input_files") as f:
        execute_code_using_files()

API docs
========

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
