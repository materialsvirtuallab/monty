---
layout: default
title: monty.os.path.md
nav_exclude: true
---

# monty.os.path module

Path based methods, e.g., which, zpath, etc.

## monty.os.path.find_exts(top, exts, exclude_dirs=None, include_dirs=None, match_mode=’basename’)

Find all files with the extension listed in exts that are located within
the directory tree rooted at top (including top itself, but excluding
‘.’ and ‘..’)

* **Parameters**
  * **top** (*str*) – Root directory
  * **exts** (*str*\* or **list** of \**strings*) – List of extensions.
  * **exclude_dirs** (*str*) – Wildcards used to exclude particular directories.
    Can be concatenated via |
  * **include_dirs** (*str*) – Wildcards used to select particular directories.
    include_dirs and exclude_dirs are mutually exclusive
  * **match_mode** (*str*) – “basename” if  match should be done on the basename.
    “abspath” for absolute path.
* **Returns**
  Absolute paths of the files.
* **Return type**
  (list of str)

Examples:

```default
# Find all pdf and ps files starting from the current directory.
find_exts(".", ("pdf", "ps"))

# Find all pdf files, exclude hidden directories and dirs whose name
# starts with `_`
find_exts(".", "pdf", exclude_dirs="_*|.*")

# Find all ps files, in the directories whose basename starts with
# output.
find_exts(".", "ps", include_dirs="output*"))
```

## monty.os.path.zpath(filename)

Returns an existing (zipped or unzipped) file path given the unzipped
version. If no path exists, returns the filename unmodified.

* **Parameters**
  **filename** – filename without zip extension
* **Returns**
  filename with a zip extension (unless an unzipped version
  exists). If filename is not found, the same filename is returned
  unchanged.