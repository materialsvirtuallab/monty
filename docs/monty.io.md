---
layout: default
title: monty.io.md
nav_exclude: true
---

# monty.io module

Augments Python’s suite of IO functions with useful transparent support for
compressed files.

## *class* monty.io.FileLock(file_name, timeout=10, delay=0.05)

Bases: `object`

A file locking mechanism that has context-manager support so you can use
it in a with statement. This should be relatively cross-compatible as it
doesn’t rely on msvcrt or fcntl for the locking.
Taken from [http://www.evanfosmark.com/2009/01/cross-platform-file-locking](http://www.evanfosmark.com/2009/01/cross-platform-file-locking)
-support-in-python/

Prepare the file locker. Specify the file to lock and optionally
the maximum timeout and the delay between each attempt to lock.


* **Parameters**

    * **file_name** – Name of file to lock.


    * **timeout** – Maximum timeout for locking. Defaults to 10.


    * **delay** – Delay between each attempt to lock. Defaults to 0.05.

### Error()

alias of `FileLockException`

### acquire()

Acquire the lock, if possible. If the lock is in use, it check again
every delay seconds. It does this until it either gets the lock or
exceeds timeout number of seconds, in which case it throws
an exception.

### release()

Get rid of the lock by deleting the lockfile.
When working in a with statement, this gets automatically
called at the end.

## *exception* monty.io.FileLockException()

Bases: `Exception`

Exception raised by FileLock.

## monty.io.get_open_fds()

Return the number of open file descriptors for current process

<!-- warning: will only work on UNIX-like OS-es. -->
## monty.io.reverse_readfile(filename: str | Path)

A much faster reverse read of file by using Python’s mmap to generate a
memory-mapped file. It is slower for very small files than
reverse_readline, but at least 2x faster for large files (the primary use
of such a method).


* **Parameters**
**filename** (*str*) – Name of file to read.


* **Yields**
Lines from the file in reverse order.

## monty.io.reverse_readline(m_file, blk_size=4096, max_mem=4000000)

Generator method to read a file line-by-line, but backwards. This allows
one to efficiently get data at the end of a file.

Based on code by Peter Astrand <[astrand@cendio.se](mailto:astrand@cendio.se)>, using modifications by
Raymond Hettinger and Kevin German.
[http://code.activestate.com/recipes/439045-read-a-text-file-backwards](http://code.activestate.com/recipes/439045-read-a-text-file-backwards)
-yet-another-implementat/

Reads file forwards and reverses in memory for files smaller than the
max_mem parameter, or for gzip files where reverse seeks are not supported.

Files larger than max_mem are dynamically read backwards.


* **Parameters**

    * **m_file** (*File*) – File stream to read (backwards)


    * **blk_size** (*int*) – The buffer size. Defaults to 4096.


    * **max_mem** (*int*) – The maximum amount of memory to involve in this
operation. This is used to determine when to reverse a file
in-memory versus seeking portions of a file. For bz2 files,
this sets the maximum block size.


* **Returns**
Generator that returns lines from the file. Similar behavior to the
file.readline() method, except the lines are returned from the back
of the file.

## monty.io.zopen(filename: str | Path, \*args, \*\*kwargs)

This function wraps around the bz2, gzip, lzma, xz and standard python’s open
function to deal intelligently with bzipped, gzipped or standard text
files.


* **Parameters**

    * **filename** (*str/Path*) – filename or pathlib.Path.


    * **\*args** – Standard args for python open(..). E.g., ‘r’ for read, ‘w’ for
write.


    * **\*\*kwargs** – Standard kwargs for python open(..).


* **Returns**
File-like object. Supports with context.