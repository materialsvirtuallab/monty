"""
Augments Python's suite of IO functions with useful transparent support for
compressed files.
"""

from __future__ import annotations

import bz2
import errno
import gzip
import io
import mmap
import os
import subprocess
import time
import warnings
from pathlib import Path
from typing import TYPE_CHECKING, Literal, cast

try:
    import lzma
except ImportError:
    lzma = None  # type: ignore[assignment]

if TYPE_CHECKING:
    from typing import IO, Iterator, Union


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
    file: str
    | Path
    | io.TextIOWrapper
    | io.BufferedReader
    | gzip.GzipFile
    | bz2.BZ2File,
) -> Literal["\r\n", "\n"]:
    """Helper function to get line ending of a file.

    This function assumes the file has a single consistent line ending.

    WARNING: as per the POSIX standard, a line is: "A sequence of zero or
    more non- characters plus a terminating character.", as such this func
    would fail if the only line misses a terminating character.
    https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html

    Returns:
        "\n": Unix line ending.
        "\r\n": Windows line ending.

    Raises:
        ValueError: If line ending is unknown.

    Warnings:
        If file is empty, "\n" would be used as default.
    """
    # TODO: Read the last N chars instead of the entire line?
    if isinstance(file, (str, Path)):
        with zopen(file, "rb") as f:
            first_line = f.readline()
    elif isinstance(file, io.TextIOWrapper):
        first_line = file.buffer.readline()
    elif isinstance(file, (io.BufferedReader, gzip.GzipFile, bz2.BZ2File)):
        first_line = file.readline()
    else:
        raise TypeError(f"Unknown file type {type(file).__name__}")

    # Reset pointer to start of file
    try:
        file.seek(0)  # type: ignore[union-attr]
    except AttributeError:
        pass

    # Return Unix "\n" line ending as default if file is empty
    if not first_line:
        warnings.warn("File is empty, return Unix line ending \n.", stacklevel=2)
        return "\n"

    if first_line.endswith(b"\r\n"):
        return "\r\n"
    if first_line.endswith(b"\n"):
        return "\n"

    # It's likely the line is missing a line ending for the first line
    raise ValueError(f"Unknown line ending in line {repr(first_line)}.")


def reverse_readfile(
    filename: Union[str, Path],
) -> Iterator[str]:
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
    # Get line ending
    l_end = _get_line_ending(filename)
    len_l_end = len(l_end)

    with zopen(filename, "rb") as file:
        if isinstance(file, (gzip.GzipFile, bz2.BZ2File)):
            for line in reversed(file.readlines()):
                # "readlines" would keep the line end character
                yield line.decode("utf-8")

        else:
            try:
                filemap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
            except ValueError:
                warnings.warn("trying to mmap an empty file.", stacklevel=2)
                return

            file_size = len(filemap)
            while file_size > 0:
                # Find line segment start and end positions
                seg_start_pos = filemap.rfind(l_end.encode(), 0, file_size)
                seg_end_pos = file_size + len_l_end

                # The first (originally) line doesn't have an ending character at its head
                if seg_start_pos == -1:
                    yield (filemap[:seg_end_pos].decode("utf-8"))

                # Skip the first match (the last line ending character)
                elif file_size != len(filemap):
                    yield (
                        filemap[seg_start_pos + len_l_end : seg_end_pos].decode("utf-8")
                    )
                file_size = seg_start_pos


def reverse_readline(
    m_file: io.BufferedReader | io.TextIOWrapper | gzip.GzipFile | bz2.BZ2File,
    blk_size: int = 4096,
    max_mem: int = 4_000_000,
) -> Iterator[str]:
    """
    Read a file backwards line-by-line, and behave similarly to
    the file.readline function. This allows one to efficiently
    get data from the end of a file.

    Supported file stream formats:
    - TextIOWrapper (text mode) | BufferedReader (binary mode)
    - gzip/bzip2 file stream

    Cases where file would be read forwards and reversed in RAM:
    - If file size is smaller than RAM usage limit (max_mem).
    - Gzip files, as reverse seeks are not supported.  # TODO: now supported

    TODO:
    - Could buffer get overly large (buffer += to_read) if
        rfind(l_end) missed several times in a row (line longer than blk_size)?
    - Test gzip seek speed (not supported previously)
    - Test bzip2 seek speed (for any improvement?)
         https://stackoverflow.com/questions/25734252/
         why-is-seeking-from-the-end-of-a-file-allowed-for-
         bzip2-files-and-not-gzip-files

    Reference:
        Based on code by Peter Astrand <astrand@cendio.se>, using
        modifications by Raymond Hettinger and Kevin German.
        http://code.activestate.com/recipes/439045-read-a-text-
        file-backwards-yet-another-implementat/

    Args:
        m_file: File stream to read (backwards).
        blk_size (int): The block size to read each time in bytes.
            Defaults to 4096.  # TODO: it's unclear what this actually controls?
        max_mem (int): Threshold to determine when to reverse a file
            in-memory versus reading blocks of a file each time.
            For bz2 files, this sets the block size.

    Yields:
        Lines from the back of the file.

    Raises:
        TypeError: If m_file is the name of the file (expect file stream).

    Warnings:
        If max_mem is smaller than blk_size.
    """
    # Check for illegal usage
    if isinstance(m_file, (str, Path)):
        raise TypeError("expect a file stream, not file name")

    # Generate line ending
    l_end: Literal["\r\n", "\n"] = _get_line_ending(m_file)
    len_l_end: Literal[1, 2] = cast(Literal[1, 2], len(l_end))

    # Check if the file stream is a buffered text stream (text instead of binary)
    is_text: bool = isinstance(m_file, io.TextIOWrapper)

    try:
        file_size: int = os.path.getsize(m_file.name)
    except AttributeError:
        # Bz2 files do not have "name" attribute.
        # Just set file_size to max_mem for now.
        file_size = max_mem + 1

    # If the file size is within desired RAM limit, just reverse it in memory.
    # Gzip files must use this method because there is no way to negative seek.
    if file_size < max_mem or isinstance(m_file, gzip.GzipFile):
        for line in reversed(m_file.readlines()):
            yield line if isinstance(line, str) else cast(bytes, line).decode("utf-8")

    else:
        # RAM limit should be greater than block size,
        # as file is read into RAM one block each time.
        if max_mem < blk_size:
            warnings.warn(f"{max_mem=} smaller than {blk_size=}", stacklevel=2)

        # For bz2 files, seek is expensive. It is therefore in our best
        # interest to maximize the block size within RAM usage limit.
        if isinstance(m_file, bz2.BZ2File):
            blk_size = min(max_mem, file_size)

        buffer: str = ""
        m_file.seek(0, 2)
        eof_pos = m_file.tell()  # Needed to skip first match

        while True:
            l_end_pos: int = buffer.rfind(l_end)
            # Pointer position (also size of remaining file)
            pt_pos: int = m_file.tell()

            # Line ending found within buffer
            if l_end_pos != -1:
                line = buffer[l_end_pos + len_l_end :]
                buffer = buffer[:l_end_pos]  # buffer doesn't include l_end

                # Skip first match (the last line ending)
                if l_end_pos != eof_pos:
                    yield line + l_end

            # Line ending not in current buffer, load next block into the buffer
            elif pt_pos > 0:
                to_read: int = min(blk_size, pt_pos)
                m_file.seek(pt_pos - to_read)
                if is_text:
                    buffer += cast(str, m_file.read(to_read))
                else:
                    buffer += cast(bytes, m_file.read(to_read)).decode("utf-8")

                # Move pointer forward
                m_file.seek(pt_pos - to_read)

                # Add a l_end to the start of file
                if pt_pos == to_read:
                    buffer = l_end + buffer

            # Start of file
            else:  # l_end_pos == -1 (not found) and pt_post == 0 (start)
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

    Warning, this will only work on UNIX-like OS.

    Returns:
        int: The number of open file descriptors for current process.
    """
    pid: int = os.getpid()
    procs: bytes = subprocess.check_output(["lsof", "-w", "-Ff", "-p", str(pid)])
    _procs: str = procs.decode("utf-8")

    return len([s for s in _procs.split("\n") if s and s[0] == "f" and s[1:].isdigit()])
