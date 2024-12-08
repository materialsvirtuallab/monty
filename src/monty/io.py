"""
Augments Python's suite of IO functions with useful transparent support for
compressed files.
"""

from __future__ import annotations

import bz2
import errno
import gzip
import io
import lzma
import mmap
import os
import subprocess
import time
import warnings
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import IO, Any, Generator, Union


class EncodingWarning(Warning): ...  # Added in Python 3.10


def zopen(
    filename: Union[str, Path],
    /,
    mode: str | None = None,
    **kwargs: Any,
) -> IO | bz2.BZ2File | gzip.GzipFile | lzma.LZMAFile:
    """
    This function wraps around `[bz2/gzip/lzma].open` and `open`
    to deal intelligently with compressed or uncompressed files.
    Supports context manager:
        `with zopen(filename, mode="rt", ...)`.

    Important Notes:
        - Default `mode` should not be used, and would not be allow
            in future versions.
        - Always explicitly specify binary/text in `mode`, i.e.
            always pass `t` or `b` in `mode`, implicit binary/text
            mode would not be allow in future versions.
        - Always provide an explicit `encoding` in text mode.

    Args:
        filename (str | Path): The file to open.
        mode (str): The mode in which the file is opened, you MUST
            explicitly specify "b" for binary or "t" for text.
        **kwargs: Additional keyword arguments to pass to `open`.

    Returns:
        TextIO | BinaryIO | bz2.BZ2File | gzip.GzipFile | lzma.LZMAFile
    """
    # Deadline for dropping implicit `mode` support
    _deadline: str = "2025-06-01"

    # Warn against default `mode`
    # TODO: remove default value of `mode` to force user to give one after deadline
    if mode is None:
        warnings.warn(
            "We strongly discourage using a default `mode`, it would be"
            f"set to `r` now but would not be allowed after {_deadline}",
            FutureWarning,
            stacklevel=2,
        )
        mode = "r"

    # Warn against implicit text/binary `mode`
    # TODO: replace warning with exception after deadline
    elif not ("b" in mode or "t" in mode):
        warnings.warn(
            "We strongly discourage using implicit binary/text `mode`, "
            f"and this would not be allowed after {_deadline}. "
            "I.e. you should pass t/b in `mode`.",
            FutureWarning,
            stacklevel=2,
        )

    # Warn against default `encoding` in text mode
    if "t" in mode and kwargs.get("encoding", None) is None:
        warnings.warn(
            "We strongly encourage explicit `encoding`, "
            "and we would use UTF-8 by default as per PEP 686",
            category=EncodingWarning,
            stacklevel=2,
        )
        kwargs["encoding"] = "utf-8"

    _name, ext = os.path.splitext(str(filename))
    ext = ext.lower()

    if ext == ".bz2":
        return bz2.open(filename, mode, **kwargs)
    if ext == ".gz":
        return gzip.open(filename, mode, **kwargs)
    if ext == ".z":
        # TODO: drop ".z" extension support after 2026-01-01
        warnings.warn(
            "Python gzip is not able to (de)compress LZW-compressed files. "
            "You should rename it to .gz. Support for the '.z' extension will "
            "be removed after 2026-01-01.",
            category=FutureWarning,
            stacklevel=2,
        )
    if ext in {".xz", ".lzma"}:
        return lzma.open(filename, mode, **kwargs)

    return open(filename, mode, **kwargs)


def reverse_readfile(filename: Union[str, Path]) -> Generator[str, str, None]:
    """
    A much faster reverse read of file by using Python's mmap to generate a
    memory-mapped file. It is slower for very small files than
    reverse_readline, but at least 2x faster for large files (the primary use
    of such a function).

    Args:
        filename (str | Path): File to read.

    Yields:
        Lines from the file in reverse order.
    """
    try:
        with zopen(filename, "rb") as file:
            if isinstance(file, (gzip.GzipFile, bz2.BZ2File)):
                for line in reversed(file.readlines()):
                    yield line.decode("utf-8").rstrip(os.linesep)
            else:
                filemap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                n = len(filemap)
                while n > 0:
                    i = filemap.rfind(os.linesep.encode(), 0, n)
                    yield filemap[i + 1 : n].decode("utf-8").rstrip(os.linesep)
                    n = i

    except ValueError:
        return


def reverse_readline(
    m_file, blk_size: int = 4096, max_mem: int = 4000000
) -> Generator[str, str, None]:
    """
    Generator function to read a file line-by-line, but backwards.
    This allows one to efficiently get data at the end of a file.

    Read file forwards and reverse in memory for files smaller than the
    max_mem parameter, or for gzip files where reverse seeks are not supported.

    Files larger than max_mem are dynamically read backwards.

    Reference:
        Based on code by Peter Astrand <astrand@cendio.se>, using modifications
        by Raymond Hettinger and Kevin German.
        http://code.activestate.com/recipes/439045-read-a-text-file-backwards
        -yet-another-implementat/

    Args:
        m_file (File): File stream to read (backwards)
        blk_size (int): The buffer size. Defaults to 4096.
        max_mem (int): The maximum amount of memory to involve in this
            operation. This is used to determine when to reverse a file
            in-memory versus seeking portions of a file. For bz2 files,
            this sets the maximum block size.

    Returns:
        Generator that yields lines from the file. Behave similarly to the
        file.readline() function, except the lines are returned from the back
        of the file.
    """
    # Check if the file stream is a bit stream or not
    is_text = isinstance(m_file, io.TextIOWrapper)

    try:
        file_size = os.path.getsize(m_file.name)
    except AttributeError:
        # Bz2 files do not have name attribute. Just set file_size to above
        # max_mem for now.
        file_size = max_mem + 1

    # If the file size is within our desired RAM use, just reverse it in memory
    # GZip files must use this method because there is no way to negative seek
    # For windows, we also read the whole file.
    if file_size < max_mem or isinstance(m_file, gzip.GzipFile) or os.name == "nt":
        for line in reversed(m_file.readlines()):
            yield line.rstrip()
    else:
        if isinstance(m_file, bz2.BZ2File):
            # for bz2 files, seeks are expensive. It is therefore in our best
            # interest to maximize the blk_size within limits of desired RAM
            # use.
            blk_size = min(max_mem, file_size)

        buf = ""
        m_file.seek(0, 2)
        lastchar = m_file.read(1) if is_text else m_file.read(1).decode("utf-8")

        trailing_newline = lastchar == os.linesep

        while True:
            newline_pos = buf.rfind(os.linesep)
            pos = m_file.tell()
            if newline_pos != -1:
                # Found a newline
                line = buf[newline_pos + 1 :]
                buf = buf[:newline_pos]
                if pos or newline_pos or trailing_newline:
                    line += os.linesep
                yield line

            elif pos:
                # Need to fill buffer
                toread = min(blk_size, pos)
                m_file.seek(pos - toread, 0)
                if is_text:
                    buf = m_file.read(toread) + buf
                else:
                    buf = m_file.read(toread).decode("utf-8") + buf
                m_file.seek(pos - toread, 0)
                if pos == toread:
                    buf = os.linesep + buf

            else:
                # Start-of-file
                return


class FileLockException(Exception):
    """Exception raised by FileLock."""


class FileLock:
    """
    A file locking mechanism that has context-manager support so you can use
    it in a with statement. This should be relatively cross-compatible as it
    doesn't rely on msvcrt or fcntl for the locking.

    Taken from http://www.evanfosmark.com/2009/01/cross-platform-file-locking
    -support-in-python/
    """

    Error = FileLockException

    def __init__(
        self, file_name: str, timeout: float = 10, delay: float = 0.05
    ) -> None:
        """
        Prepare the file locker. Specify the file to lock and optionally
        the maximum timeout and the delay between each attempt to lock.

        Args:
            file_name (str): Name of file to lock.
            timeout (float): Maximum timeout in second for locking. Defaults to 10.
            delay (float): Delay in second between each attempt to lock. Defaults to 0.05.
        """
        self.file_name = os.path.abspath(file_name)
        self.lockfile = f"{os.path.abspath(file_name)}.lock"
        self.timeout = timeout
        self.delay = delay
        self.is_locked = False

        if self.delay > self.timeout or self.delay <= 0 or self.timeout <= 0:
            raise ValueError("delay and timeout must be positive with delay <= timeout")

    def __enter__(self):
        """
        Activated when used in the with statement. Should automatically
        acquire a lock to be used in the with block.
        """
        if not self.is_locked:
            self.acquire()
        return self

    def __exit__(self, type_, value, traceback):
        """
        Activated at the end of the with statement. It automatically releases
        the lock if it isn't locked.
        """
        if self.is_locked:
            self.release()

    def __del__(self):
        """
        Make sure that the FileLock instance doesn't leave a lockfile
        lying around.
        """
        self.release()

    def acquire(self) -> None:
        """
        Acquire the lock, if possible. If the lock is in use, it check again
        every `delay` seconds. It does this until it either gets the lock or
        exceeds `timeout` number of seconds, in which case it throws
        an exception.
        """
        start_time = time.time()
        while True:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                break
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
                if (time.time() - start_time) >= self.timeout:
                    raise FileLockException(f"{self.lockfile}: Timeout occurred.")
                time.sleep(self.delay)

        self.is_locked = True

    def release(self) -> None:
        """
        Get rid of the lock by deleting the lockfile.
        When working in a `with` statement, this gets automatically
        called at the end.
        """
        if self.is_locked:
            os.close(self.fd)
            os.unlink(self.lockfile)
            self.is_locked = False


def get_open_fds() -> int:
    """
    Get the number of open file descriptors for current process.

    Warnings:
        Will only work on UNIX-like OS-es.

    Returns:
        int: The number of open file descriptors for current process.
    """
    pid: int = os.getpid()
    procs: bytes = subprocess.check_output(["lsof", "-w", "-Ff", "-p", str(pid)])
    _procs: str = procs.decode("utf-8")

    return len([s for s in _procs.split("\n") if s and s[0] == "f" and s[1:].isdigit()])
