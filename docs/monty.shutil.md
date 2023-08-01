---
layout: default
title: monty.shutil.md
nav_exclude: true
---

# monty.shutil module

Copying and zipping utilities. Works on directories mostly.


### monty.shutil.compress_dir(path, compression='gz')
Recursively compresses all files in a directory. Note that this
compresses all files singly, i.e., it does not create a tar archive. For
that, just use Python tarfile class.


* **Parameters**


    * **path** (*str*) – Path to parent directory.


    * **compression** (*str*) – A compression mode. Valid options are “gz” or
    “bz2”. Defaults to gz.



### monty.shutil.compress_file(filepath, compression='gz')
Compresses a file with the correct extension. Functions like standard
Unix command line gzip and bzip2 in the sense that the original
uncompressed files are not retained.


* **Parameters**


    * **filepath** (*str*) – Path to file.


    * **compression** (*str*) – A compression mode. Valid options are “gz” or
    “bz2”. Defaults to “gz”.



### monty.shutil.copy_r(src, dst)
Implements a recursive copy function similar to Unix’s “cp -r” command.
Surprisingly, python does not have a real equivalent. shutil.copytree
only works if the destination directory is not present.


* **Parameters**


    * **src** (*str*) – Source folder to copy.


    * **dst** (*str*) – Destination folder.



### monty.shutil.decompress_dir(path)
Recursively decompresses all files in a directory.


* **Parameters**

    **path** (*str*) – Path to parent directory.



### monty.shutil.decompress_file(filepath)
Decompresses a file with the correct extension. Automatically detects
gz, bz2 or z extension.


* **Parameters**


    * **filepath** (*str*) – Path to file.


    * **compression** (*str*) – A compression mode. Valid options are “gz” or
    “bz2”. Defaults to “gz”.



### monty.shutil.gzip_dir(path, compresslevel=6)
Gzips all files in a directory. Note that this is different from
shutil.make_archive, which creates a tar archive. The aim of this method
is to create gzipped files that can still be read using common Unix-style
commands like zless or zcat.


* **Parameters**


    * **path** (*str*) – Path to directory.


    * **compresslevel** (*int*) – Level of compression, 1-9. 9 is default for
    GzipFile, 6 is default for gzip.



### monty.shutil.remove(path, follow_symlink=False)
Implements a remove function that will delete files, folder trees and
symlink trees

1.) Remove a file
2.) Remove a symlink and follow into with a recursive rm if follow_symlink
3.) Remove directory with rmtree


* **Parameters**


    * **path** (*str*) – path to remove


    * **follow_symlink** (*bool*) – follow symlinks and removes whatever is in them