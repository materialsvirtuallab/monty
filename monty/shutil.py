"""Copying and zipping utilities. Works on directories mostly."""
from __future__ import annotations

import os
import shutil
import warnings
from gzip import GzipFile
from pathlib import Path
from typing import Literal

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
    os.makedirs(absdst, exist_ok=True)
    for f in os.listdir(abssrc):
        fpath = Path(abssrc, f)
        if Path(fpath).is_file():
            shutil.copy(fpath, absdst)
        elif str(fpath) not in str(absdst):
            copy_r(fpath, Path(absdst, f))
        else:
            warnings.warn(f"Cannot copy {fpath} to itself")


def gzip_dir(path: str | Path, compresslevel: int = 6) -> None:
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
            full_f = Path(root, f).resolve()
            if Path(f).suffix.lower() != ".gz" and not full_f.is_dir():
                with open(full_f, "rb") as f_in, GzipFile(f"{full_f}.gz", "wb", compresslevel=compresslevel) as f_out:
                    shutil.copyfileobj(f_in, f_out)
                shutil.copystat(full_f, f"{full_f}.gz")
                os.remove(full_f)


def compress_file(filepath: str | Path, compression: Literal["gz", "bz2"] = "gz") -> None:
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
    if filepath.suffix.lower() != f".{compression}":
        with open(filepath, "rb") as f_in, zopen(f"{filepath}.{compression}", "wb") as f_out:
            f_out.writelines(f_in)
        os.remove(filepath)


def compress_dir(path: str | Path, compression: Literal["gz", "bz2"] = "gz") -> None:
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
            compress_file(Path(parent, f), compression=compression)

    return None


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
    file_ext = filepath.suffix
    if file_ext.lower() in [".bz2", ".gz", ".z"] and filepath.is_file():
        decompressed_file = Path(str(filepath).removesuffix(file_ext))
        with zopen(filepath, "rb") as f_in, open(decompressed_file, "wb") as f_out:
            f_out.writelines(f_in)
        os.remove(filepath)

        return str(decompressed_file)
    return None


def decompress_dir(path: str | Path) -> None:
    """
    Recursively decompresses all files in a directory.

    Args:
        path (str | Path): Path to parent directory.
    """
    path = Path(path)
    for parent, _, files in os.walk(path):
        for f in files:
            decompress_file(Path(parent, f))


def remove(path: str | Path, follow_symlink: bool = False) -> None:
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
        Path.unlink(path)
    else:
        shutil.rmtree(path)
