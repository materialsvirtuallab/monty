from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Project'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import os


def which(cmd):
    """
    Returns full path to a executable.

    Args:
        cmd (str): Executable command to search for.

    Returns:
        (str) Full path to command. None if it is not found.

    Example::

        full_path_to_python = which("python")
    """
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(cmd)
    if fpath:
        if is_exe(cmd):
            return cmd
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, cmd)
            if is_exe(exe_file):
                return exe_file
    return None


def zpath(filename):
    """
    Returns an existing (zipped or unzipped) file path given the unzipped
    version. If no path exists, returns the filename unmodified.

    Args:
        filename: filename without zip extension

    Returns:
        filename with a zip extension (unless an unzipped version
        exists). If filename is not found, the same filename is returned
        unchanged.
    """
    for ext in ["", '.gz', '.GZ', '.bz2', '.BZ2', '.z', '.Z']:
        zfilename = "{}{}".format(filename, ext)
        if os.path.exists(zfilename):
            return zfilename
    return filename