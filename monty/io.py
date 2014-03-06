"""
Augments Python's suite of IO functions with useful transparent support for
compressed files.
"""

from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'

import os
from bz2 import BZ2File
from gzip import GzipFile

from monty.tempfile import ScratchDir as ScrDir
from monty.dev import deprecated


def zopen(filename, *args, **kwargs):
    """
    This function wraps around the bz2, gzip and standard python's open
    function to deal intelligently with bzipped, gzipped or standard text
    files.

    Args:
        filename (str): filename
        \*args: Standard args for python open(..). E.g., 'r' for read, 'w' for
            write.
        \*\*kwargs: Standard kwargs for python open(..).

    Returns:
        File-like object. Supports with context.
    """
    file_ext = filename.split(".")[-1].upper()
    if file_ext == "BZ2":
        return BZ2File(filename, *args, **kwargs)
    elif file_ext in ("GZ", "Z"):
        return GzipFile(filename, *args, **kwargs)
    else:
        return open(filename, *args, **kwargs)


def reverse_readline(m_file, blk_size=4096, max_mem=4000000):
    """
    Generator method to read a file line-by-line, but backwards. This allows
    one to efficiently get data at the end of a file.

    Based on code by Peter Astrand <astrand@cendio.se>, using modifications by
    Raymond Hettinger and Kevin German.
    http://code.activestate.com/recipes/439045-read-a-text-file-backwards
    -yet-another-implementat/

    Reads file forwards and reverses in memory for files smaller than the
    max_mem parameter, or for gzip files where reverse seeks are not supported.

    Files larger than max_mem are dynamically read backwards.

    Args:
        m_file (File): File stream to read (backwards)
        blk_size (int): The buffer size. Defaults to 4096.
        max_mem (int): The maximum amount of memory to involve in this
            operation. This is used to determine when to reverse a file
            in-memory versus seeking portions of a file. For bz2 files,
            this sets the maximum block size.

    Returns:
        Generator that returns lines from the file. Similar behavior to the
        file.readline() method, except the lines are returned from the back
        of the file.
    """

    file_size = os.path.getsize(m_file.name)

    # If the file size is within our desired RAM use, just reverse it in memory
    # GZip files must use this method because there is no way to negative seek
    if file_size < max_mem or isinstance(m_file, GzipFile):
        for line in reversed(m_file.readlines()):
            yield line.rstrip()
    else:
        if isinstance(m_file, BZ2File):
            # for bz2 files, seeks are expensive. It is therefore in our best
            # interest to maximize the blk_size within limits of desired RAM
            # use.
            blk_size = min(max_mem, file_size)

        buf = ""
        m_file.seek(0, 2)
        lastchar = m_file.read(1)
        trailing_newline = (lastchar == "\n")

        while 1:
            newline_pos = buf.rfind("\n")
            pos = m_file.tell()
            if newline_pos != -1:
                # Found a newline
                line = buf[newline_pos + 1:]
                buf = buf[:newline_pos]
                if pos or newline_pos or trailing_newline:
                    line += "\n"
                yield line
            elif pos:
                # Need to fill buffer
                toread = min(blk_size, pos)
                m_file.seek(pos - toread, 0)
                buf = m_file.read(toread) + buf
                m_file.seek(pos - toread, 0)
                if pos == toread:
                    buf = "\n" + buf
            else:
                # Start-of-file
                return


@deprecated(ScrDir)
class ScratchDir(ScrDir):
    pass
