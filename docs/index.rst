.. monty documentation master file, created by
   sphinx-quickstart on Tue Nov 15 00:13:52 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Monty - The Missing Complement to Python
========================================

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

Monty is tested for both Python 2.7 and Python 3+ compatibility.

Latest Change Log
=================

v0.1.0
------
1. Ensure Python 3+ compatibility.
2. Travis testing implemented.

v0.0.5
------
1. First official alpha release with unittests and docs.

v0.0.2
------
1. Added several decorators and utilities.

:doc:`Older versions </changelog>`

Installing monty
================

The version at the Python Package Index (PyPI) is always the latest stable
release that will be hopefully, be relatively bug-free. The easiest way to
install monty on any system is to use easy_install or pip, as follows::

    easy_install monty

or::

    pip install monty

Usage
=====

Unlike most other modules, the organization of Monty mirrors that of the
standard Python library where possible. This style is adopted so that that
it is almost always obvious where a particular method or function
will reside. There are two recommended ways of using Monty.

First method - import the monty root::

    import monty as mt
    with mt.io.zopen("src.gz") as f:
        data = f.read()
    with mt.io.zopen("dest.bz2", "wb") as f:
        f.write(data)

Second method - import specific functions as needed::

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

API docs
--------

.. toctree::

   monty

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


.. _`pymatgen's Google Groups page`: https://groups.google.com/forum/?fromgroups#!forum/pymatgen/
.. _`PyPI` : http://pypi.python.org/pypi/pymatgen
.. _`Github page`: https://github.com/materialsproject/pymatgen/issues
