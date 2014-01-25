from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = "Copyright 2014, The Materials Virtual Lab"
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import os
import shutil


def copy_r(src, dst):
    """
    Implements a recursive copy function similar to Unix's "cp -r" command.
    Surprisingly, python does not have a real equivalent. shutil.copytree
    only works if the destination directory is not present.

    Args:
        src (str): Source folder to copy.
        dst (str): Destination folder.
    """
    for parent, subdir, files in os.walk(src):
        parent = os.path.relpath(parent)
        realdst = dst if parent == "." else os.path.join(dst, parent)
        try:
            os.makedirs(realdst)
        except Exception as ex:
            pass
        for f in files:
            shutil.copy(os.path.join(parent, f), realdst)