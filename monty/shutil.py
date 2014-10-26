from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import os
import shutil
import warnings
from gzip import GzipFile


def copy_r(src, dst):
    """
    Implements a recursive copy function similar to Unix's "cp -r" command.
    Surprisingly, python does not have a real equivalent. shutil.copytree
    only works if the destination directory is not present.

    Args:
        src (str): Source folder to copy.
        dst (str): Destination folder.
    """

    abssrc = os.path.abspath(src)
    absdst = os.path.abspath(dst)
    try:
        os.makedirs(absdst)
    except OSError:
        # If absdst exists, an OSError is raised. We ignore this error.
        pass
    for f in os.listdir(abssrc):
        fpath = os.path.join(abssrc, f)
        if os.path.isfile(fpath):
            shutil.copy(fpath, absdst)
        elif not absdst.startswith(fpath):
            copy_r(fpath, os.path.join(absdst, f))
        else:
            warnings.warn("Cannot copy %s to itself" % fpath)


def gzip_dir(path):
    """
    Gzips all files in a directory.

    Args:
        path (str): Path to directory.
    """
    for f in os.listdir(path):
        if not f.lower().endswith("gz"):
            with open(f, 'rb') as f_in, \
                    GzipFile('{}.gz'.format(f), 'wb') as f_out:
                f_out.writelines(f_in)
            os.remove(f)


def compress_file(filepath, compression="gz"):
    """
    Compresses a file with the correct extension. Functions like standard
    Unix command line gzip and bzip2 in the sense that the original
    uncompressed files are not retained.

    Args:
        filepath (str): Path to file.
        compression (str): A compression mode. Valid options are "gz" or
            "bz2". Defaults to "gz".
    """
    if compression not in ["gz", "bz2"]:
        raise ValueError("Supported compression formats are 'gz' and 'bz2'.")
    from monty.io import zopen
    if not filepath.lower().endswith(".%s" % compression):
        with open(filepath, 'rb') as f_in, \
                zopen('%s.%s' % (filepath, compression), 'wb') as f_out:
            f_out.writelines(f_in)
        os.remove(filepath)


def compress_dir(path, compression="gz"):
    """
    Recursively compresses all files in a directory. Note that this
    compresses all files singly, i.e., it does not create a tar archive. For
    that, just use Python tarfile class.

    Args:
        path (str): Path to parent directory.
        compression (str): A compression mode. Valid options are "gz" or
            "bz2". Defaults to gz.
    """
    for parent, subdirs, files in os.walk(path):
        for f in files:
            compress_file(os.path.join(parent, f), compression=compression)


def decompress_file(filepath):
    """
    Decompresses a file with the correct extension. Automatically detects
    gz, bz2 or z extension.

    Args:
        filepath (str): Path to file.
        compression (str): A compression mode. Valid options are "gz" or
            "bz2". Defaults to "gz".
    """
    toks = filepath.split(".")
    file_ext = toks[-1].upper()
    from monty.io import zopen
    if file_ext in ["BZ2", "GZ", "Z"]:
        with open(".".join(toks[0:-1]), 'wb') as f_out, \
                zopen(filepath, 'rb') as f_in:
            f_out.writelines(f_in)
        os.remove(filepath)


def decompress_dir(path):
    """
    Recursively decompresses all files in a directory.

    Args:
        path (str): Path to parent directory.
    """
    for parent, subdirs, files in os.walk(path):
        for f in files:
            decompress_file(os.path.join(parent, f))

