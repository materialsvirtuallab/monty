"""
Augments Python's suite of IO functions with useful transparent support for
compressed files.
"""

from __future__ import annotations

import bz2
import errno
import gzip
import io

try:
    import lzma
except ImportError:
    lzma = None  # type: ignore[assignment]
import mmap
import os
import subprocess
import time
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import IO, Generator, Literal, Union


def zopen(filename: Union[str, Path], *args, **kwargs) -> IO:
    """
    This function wraps around the bz2, gzip, lzma, xz and standard Python's open
    function to deal intelligently with bzipped, gzipped or standard text
    files.

    Args:
        filename (str/Path): filename or pathlib.Path.
        *args: Standard args for Python open(..). E.g., 'r' for read, 'w' for
            write.
        **kwargs: Standard kwargs for Python open(..).

    Returns:
        File-like object. Supports with context.
    """
    if filename is not None and isinstance(filename, Path):
        filename = str(filename)

    _name, ext = os.path.splitext(filename)
    ext = ext.upper()
    if ext == ".BZ2":
        return bz2.open(filename, *args, **kwargs)
    if ext in {".GZ", ".Z"}:
        return gzip.open(filename, *args, **kwargs)
    if lzma is not None and ext in {".XZ", ".LZMA"}:
        return lzma.open(filename, *args, **kwargs)
    return open(filename, *args, **kwargs)


def _get_line_ending(
    file: str | Path | io.TextIOWrapper,
) -> Literal["\r\n", "\n", "\r"]:
    """Helper function to get line ending of a file.

    This function assumes the file has a single consistent line ending.

    Returns:
        "\n": Unix line ending.
        "\r\n": Windows line ending.
        "\r": Classic MacOS line ending.

    Raises:
        ValueError: If file is empty or line ending is unknown.
    """
    if isinstance(file, (str, Path)):
        with open(file, "rb") as f:
            first_line = f.readline()
    elif isinstance(file, io.TextIOWrapper):
        first_line = file.buffer.readline()

    if not first_line:
        raise ValueError("empty file.")

    if first_line.endswith(b"\r\n"):
        return "\r\n"
    elif first_line.endswith(b"\n"):
        return "\n"
    elif first_line.endswith(b"\r"):
        return "\r"
    else:
        raise ValueError(f"Unknown line ending in file {repr(first_line)}.")


def reverse_readfile(
    filename: Union[str, Path],
    l_end: Literal["AUTO"] | str = "AUTO",
) -> Generator[str, str, None]:
    """
    A much faster reverse read of file by using Python's mmap to generate a
    memory-mapped file. It is slower for very small files than
    reverse_readline, but at least 2x faster for large files (the primary use
    of such a function).

    Args:
        filename (str | Path): File to read.
        l_end ("AUTO" | str): Line ending. Use "AUTO" to
            automatically decide line ending based on OS.

    Yields:
        Lines from the file in reverse order.
    """
    # Generate line ending
    l_end = os.linesep if "AUTO" else l_end

    try:
        with zopen(filename, "rb") as file:
            if isinstance(file, (gzip.GzipFile, bz2.BZ2File)):
                for line in reversed(file.readlines()):
                    yield line.decode("utf-8").rstrip()

            else:
                filemap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
                n = len(filemap)
                while n > 0:
                    i = filemap.rfind(l_end.encode(), 0, n)
                    yield filemap[i + 1 : n].decode("utf-8").rstrip()
                    n = i

    except ValueError:
        return


def reverse_readline(
    m_file,  # TODO: add type
    blk_size: int = 4096,
    max_mem: int = 4000000,
    l_end: Literal["AUTO"] | str = "AUTO",
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
        blk_size (int): The buffer size in bytes. Defaults to 4096.
        max_mem (int): The maximum amount of memory to involve in this
            operation. This is used to determine when to reverse a file
            in-memory versus seeking portions of a file. For bz2 files,
            this sets the maximum block size.
        l_end ("AUTO" | str): Line ending. Use "AUTO" to
            automatically decide line ending based on OS.

    Yields:
        Lines from the file. Behave similarly to the file.readline function,
        except the lines are returned from the back of the file.
    """
    # Generate line ending
    l_end = os.linesep if "AUTO" else l_end

    # Check if the file stream is a buffered text stream
    is_text = isinstance(m_file, io.TextIOWrapper)

    try:
        file_size = os.path.getsize(m_file.name)
    except AttributeError:
        # Bz2 files do not have name attribute.
        # Just set file_size to max_mem for now.
        file_size = max_mem + 1

    # If the file size is within desired RAM limit, just reverse it in memory.
    # GZip files must use this method because there is no way to negative seek.
    # For windows, we also read the whole file.
    if file_size < max_mem or isinstance(m_file, gzip.GzipFile) or os.name == "nt":
        for line in reversed(m_file.readlines()):
            yield line.rstrip()

    else:
        if isinstance(m_file, bz2.BZ2File):
            # For bz2 files, seeks are expensive. It is therefore in our best
            # interest to maximize the blk_size within limits of desired RAM
            # use.
            blk_size = min(max_mem, file_size)

        buf = ""
        m_file.seek(0, 2)
        last_char = m_file.read(1) if is_text else m_file.read(1).decode("utf-8")

        trailing_newline = last_char == l_end

        while True:
            newline_pos = buf.rfind(l_end)
            pos = m_file.tell()
            if newline_pos != -1:
                # Found a newline
                line = buf[newline_pos + 1 :]
                buf = buf[:newline_pos]
                if pos or newline_pos or trailing_newline:
                    line += l_end
                yield line

            elif pos:
                # Need to fill buffer
                to_read = min(blk_size, pos)
                m_file.seek(pos - to_read, 0)
                if is_text:
                    buf = m_file.read(to_read) + buf
                else:
                    buf = m_file.read(to_read).decode("utf-8") + buf
                m_file.seek(pos - to_read, 0)
                if pos == to_read:
                    buf = l_end + buf

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
