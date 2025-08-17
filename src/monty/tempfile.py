"""
Temporary directory and file creation utilities.
"""

from __future__ import annotations

import os
import tempfile
from typing import TYPE_CHECKING

from monty.shutil import copy_r, gzip_dir, remove

if TYPE_CHECKING:
    from pathlib import Path
    from typing import ClassVar, Union


class ScratchDir:
    """
    Notes:
        With effect from Python 3.2, tempfile.TemporaryDirectory already
        implements much of the functionality of ScratchDir. However, it does
        not provide options for copying of files to and from (though it is
        possible to do this with other methods provided by shutil).

    Creates a "with" context manager that automatically handles creation of
    temporary directories (utilizing Python's build in temp directory
    functions) and cleanup when done. This improves on Python's built in
    functions by allowing for truly temporary workspace that are deleted
    when it is done. The way it works is as follows:

    1. Create a temp dir in specified root path.
    2. Optionally copy input files from current directory to temp dir.
    3. Change to temp dir.
    4. User performs specified operations.
    5. Optionally copy generated output files back to original directory.
    6. Change back to original directory.
    7. Delete temp dir.
    """

    SCR_LINK: ClassVar[str] = "scratch_link"

    def __init__(
        self,
        rootpath: Union[str, Path, None],
        create_symbolic_link: bool = False,
        copy_from_current_on_enter: bool = False,
        copy_to_current_on_exit: bool = False,
        gzip_on_exit: bool = False,
        delete_removed_files: bool = True,
    ) -> None:
        """
        Initializes scratch directory given a **root** path. There is no need
        to try to create unique directory names. The code will generate a
        temporary sub directory in the rootpath. The way to use this is using a
        with context manager. Example::

            with ScratchDir("/scratch"):
                do_something()

        If the root path does not exist or is None, this will function as a
        simple pass through, i.e., nothing happens.

        Args:
            rootpath (str/Path): Path in which to create temp subdirectories.
                If this is None, no temp directories will be created and
                this will just be a simple pass through.
            create_symbolic_link (bool): Whether to create a symbolic link in
                the current working directory to the scratch directory
                created.
            copy_from_current_on_enter (bool): Whether to copy all files from
                the current directory (recursively) to the temp dir at the
                start, e.g., if input files are needed for performing some
                actions. Defaults to False.
            copy_to_current_on_exit (bool): Whether to copy files from the
                scratch to the current directory (recursively) at the end. E
                .g., if output files are generated during the operation.
                Defaults to False.
            gzip_on_exit (bool): Whether to gzip the files generated in the
                ScratchDir before copying them back.
                Defaults to False.
            delete_removed_files (bool): Whether to delete files in the cwd
                that are removed from the tmp dir.
                Defaults to True.
        """
        self.rootpath: str | None = (
            None if rootpath is None else os.path.abspath(rootpath)
        )
        self.cwd: str = os.getcwd()

        self.create_symbolic_link: bool = create_symbolic_link
        self.start_copy: bool = copy_from_current_on_enter
        self.end_copy: bool = copy_to_current_on_exit
        self.gzip_on_exit: bool = gzip_on_exit
        self.delete_removed_files: bool = delete_removed_files

    def __enter__(self) -> str:
        tempdir = self.cwd
        if self.rootpath is not None and os.path.exists(self.rootpath):
            tempdir = tempfile.mkdtemp(dir=self.rootpath)
            self.tempdir = os.path.abspath(tempdir)
            if self.start_copy:
                copy_r(self.cwd, tempdir)
            if self.create_symbolic_link:
                os.symlink(tempdir, ScratchDir.SCR_LINK)
            os.chdir(tempdir)
        return tempdir

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.rootpath is not None and os.path.exists(self.rootpath):
            if self.end_copy:
                files = set(os.listdir(self.tempdir))
                orig_files = set(os.listdir(self.cwd))

                # gzip files
                if self.gzip_on_exit:
                    gzip_dir(self.tempdir)

                # copy files over
                copy_r(self.tempdir, self.cwd)

                # Delete any files that are now gone
                if self.delete_removed_files:
                    for f in orig_files - files:
                        fpath = os.path.join(self.cwd, f)
                        remove(fpath)

            os.chdir(self.cwd)
            remove(self.tempdir)
            if self.create_symbolic_link and os.path.islink(ScratchDir.SCR_LINK):
                os.remove(ScratchDir.SCR_LINK)
