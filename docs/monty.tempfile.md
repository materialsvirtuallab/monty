---
layout: default
title: monty.tempfile.md
nav_exclude: true
---

# monty.tempfile module

Temporary directory and file creation utilities.

## *class* monty.tempfile.ScratchDir(rootpath, create_symbolic_link=False, copy_from_current_on_enter=False, copy_to_current_on_exit=False, gzip_on_exit=False, delete_removed_files=True)

Bases: `object`

**NOTE**: With effect from Python 3.2, tempfile.TemporaryDirectory already
implements much of the functionality of ScratchDir. However, it does
not provide options for copying of files to and from (though it is
possible to do this with other methods provided by shutil).

Creates a “with” context manager that automatically handles creation of
temporary directories (utilizing Python’s build in temp directory
functions) and cleanup when done. This improves on Python’s built in
functions by allowing for truly temporary workspace that are deleted
when it is done. The way it works is as follows:

1. Create a temp dir in specified root path.
2. Optionally copy input files from current directory to temp dir.
3. Change to temp dir.
4. User performs specified operations.
5. Optionally copy generated output files back to original directory.
6. Change back to original directory.
7. Delete temp dir.

Initializes scratch directory given a **root** path. There is no need
to try to create unique directory names. The code will generate a
temporary sub directory in the rootpath. The way to use this is using a
with context manager. Example:

```default
with ScratchDir("/scratch"):
    do_something()
```

If the root path does not exist or is None, this will function as a
simple pass through, i.e., nothing happens.

* **Parameters**
  * **rootpath** (*str/Path*) – Path in which to create temp subdirectories.
    If this is None, no temp directories will be created and
    this will just be a simple pass through.
  * **create_symbolic_link** (*bool*) – Whether to create a symbolic link in
    the current working directory to the scratch directory
    created.
  * **copy_from_current_on_enter** (*bool*) – Whether to copy all files from
    the current directory (recursively) to the temp dir at the
    start, e.g., if input files are needed for performing some
    actions. Defaults to False.
  * **copy_to_current_on_exit** (*bool*) – Whether to copy files from the
    scratch to the current directory (recursively) at the end. E
    .g., if output files are generated during the operation.
    Defaults to False.
  * **gzip_on_exit** (*bool*) – Whether to gzip the files generated in the
    ScratchDir before copying them back.
    Defaults to False.
  * **delete_removed_files** (*bool*) – Whether to delete files in the cwd
    that are removed from the tmp dir.
    Defaults to True

### SCR_LINK(_ = ‘scratch_link_ )