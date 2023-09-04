"""Copying and zipping utilities. Works on directories mostly."""
from __future__ import annotations

import os
import shutil
import warnings
from gzip import GzipFile
from pathlib import Path

from .io import zopen


def copy_r(src: str | Path, dst: str | Path) -> None:
    """
    Implements a recursive copy function similar to Unix's "cp -r" command.
    Surprisingly, python does not have a real equivalent. shutil.copytree
    only works if the destination directory is not present.

    Args:
        src (str | Path): Source folder to copy.
        dst (str | Path): Destination folder.
    """
    src = Path(src)
    dst = Path(dst)
    abssrc = src.resolve()
    absdst = dst.resolve()
    try:
        os.makedirs(absdst)
    except OSError:
        # If absdst exists, an OSError is raised. We ignore this error.
        pass
    for f in os.listdir(abssrc):
        fpath = Path(abssrc, f)
        if Path(fpath).is_file():
            shutil.copy(fpath, absdst)
        elif not absdst.startswith(fpath):
            copy_r(fpath, Path(absdst, f))
        else:
            warnings.warn(f"Cannot copy {fpath} to itself")


def gzip_dir(path: str | Path, compresslevel=6):
    """
    Gzips all files in a directory. Note that this is different from
    shutil.make_archive, which creates a tar archive. The aim of this method
    is to create gzipped files that can still be read using common Unix-style
    commands like zless or zcat.

    Args:
        path (str | Path): Path to directory.
        compresslevel (int): Level of compression, 1-9. 9 is default for
            GzipFile, 6 is default for gzip.
    """
    path = Path(path)
    for root, _, files in os.walk(path):
        for f in files:
            full_f = os.path.abspath(os.path.join(root, f))
            if not f.lower().endswith("gz") and not os.path.isdir(full_f):
                with open(full_f, "rb") as f_in, GzipFile(f"{full_f}.gz", "wb", compresslevel=compresslevel) as f_out:
                    shutil.copyfileobj(f_in, f_out)
                shutil.copystat(full_f, f"{full_f}.gz")
                os.remove(full_f)


def compress_file(filepath: str | Path, compression="gz"):
    """
    Compresses a file with the correct extension. Functions like standard
    Unix command line gzip and bzip2 in the sense that the original
    uncompressed files are not retained.

    Args:
        filepath (str | Path): Path to file.
        compression (str): A compression mode. Valid options are "gz" or
            "bz2". Defaults to "gz".
    """
    filepath = Path(filepath)
    if compression not in ["gz", "bz2"]:
        raise ValueError("Supported compression formats are 'gz' and 'bz2'.")
    if not filepath.lower().endswith(f".{compression}"):
        with open(filepath, "rb") as f_in, zopen(f"{filepath}.{compression}", "wb") as f_out:
            f_out.writelines(f_in)
        os.remove(filepath)


def compress_dir(path: str | Path, compression="gz"):
    """
    Recursively compresses all files in a directory. Note that this
    compresses all files singly, i.e., it does not create a tar archive. For
    that, just use Python tarfile class.

    Args:
        path (str | Path): Path to parent directory.
        compression (str): A compression mode. Valid options are "gz" or
            "bz2". Defaults to gz.
    """
    path = Path(path)
    for parent, _, files in os.walk(path):
        for f in files:
            compress_file(os.path.join(parent, f), compression=compression)


def decompress_file(filepath: str | Path) -> str | None:
    """
    Decompresses a file with the correct extension. Automatically detects
    gz, bz2 or z extension.

    Args:
        filepath (str): Path to file.

    Returns:
        str: The decompressed file path.
    """
    filepath = Path(filepath)
    toks = str(filepath).split(".")
    file_ext = toks[-1].upper()
    if file_ext in ["BZ2", "GZ", "Z"] and filepath.is_file():
        decompressed_file = ".".join(toks[0:-1])
        with zopen(filepath, "rb") as f_in, open(decompressed_file, "wb") as f_out:
            f_out.writelines(f_in)
        os.remove(filepath)

        return decompressed_file
    return None


def decompress_dir(path: str | Path):
    """
    Recursively decompresses all files in a directory.

    Args:
        path (str | Path): Path to parent directory.
    """
    path = Path(path)
    for parent, _, files in os.walk(path):
        for f in files:
            decompress_file(Path(parent, f))


def remove(path: str | Path, follow_symlink=False):
    """
    Implements a remove function that will delete files, folder trees and
    symlink trees.

    1.) Remove a file
    2.) Remove a symlink and follow into with a recursive rm if follow_symlink
    3.) Remove directory with rmtree

    Args:
        path (str | Path): path to remove
        follow_symlink(bool): follow symlinks and removes whatever is in them
    """
    path = Path(path)
    if path.is_file():
        os.remove(path)
    elif path.is_symlink():
        if follow_symlink:
            remove(os.readlink(path))
        os.unlink(path)
    else:
        shutil.rmtree(path)
