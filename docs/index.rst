.. monty documentation master file, created by
   sphinx-quickstart on Tue Nov 15 00:13:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Monty - The Missing Complement to Python
========================================

.. image:: https://travis-ci.org/materialsvirtuallab/monty.png?branch=master

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

Monty is tested to work on Python 2.7, 3.x.

Latest Change Log
=================

v0.5.4
------
1. Addition of many help functions in string, itertools, etc. (Matteo).
2. NullFile and NullStream in monty.design_patterns (Matteo).
3. FileLock in monty.io (Matteo)

v0.5.3
------
1. Minor efficiency improvement.

v0.5.2
------
1. Add unicode2str and str2unicode in monty.string.

v0.5.0
------
1. Completely rewritten zopen which supports the "rt" keyword of Python 3
   even when used in Python 2.
2. monty.string now has a marquee method which centers a string
   (contributed by Matteo).
3. Monty now supports only Python >= 3.3 as well as Python 2.7. Python 3.2
   support is now dropped.

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
follows::

    The MIT License (MIT)
    Copyright (c) 2011-2012 MIT & LBNL

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software")
    , to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
