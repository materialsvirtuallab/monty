---
layout: default
title: monty.serialization.md
nav_exclude: true
---

# monty.serialization module

This module implements serialization support for common formats such as json
and yaml.


### monty.serialization.dumpfn(obj, fn, \*args, fmt=None, \*\*kwargs)
Dump to a json/yaml directly by filename instead of a
File-like object. File may also be a BZ2 (“.BZ2”) or GZIP (“.GZ”, “.Z”)
compressed file.
For YAML, ruamel.yaml must be installed. The file type is automatically
detected from the file extension (case insensitive). YAML is assumed if the
filename contains “.yaml” or “.yml”.
Msgpack is assumed if the filename contains “.mpk”.
JSON is otherwise assumed.


* **Parameters**


    * **obj** (*object*) – Object to dump.


    * **fn** (*str/Path*) – filename or pathlib.Path.


    * **\*args** – Any of the args supported by json/yaml.dump.


    * **\*\*kwargs** – Any of the kwargs supported by json/yaml.dump.



* **Returns**

    (object) Result of json.load.



### monty.serialization.loadfn(fn, \*args, fmt=None, \*\*kwargs)
Loads json/yaml/msgpack directly from a filename instead of a
File-like object. File may also be a BZ2 (“.BZ2”) or GZIP (“.GZ”, “.Z”)
compressed file.
For YAML, ruamel.yaml must be installed. The file type is automatically
detected from the file extension (case insensitive).
YAML is assumed if the filename contains “.yaml” or “.yml”.
Msgpack is assumed if the filename contains “.mpk”.
JSON is otherwise assumed.


* **Parameters**


    * **fn** (*str/Path*) – filename or pathlib.Path.


    * **\*args** – Any of the args supported by json/yaml.load.


    * **fmt** (*string*) – If specified, the fmt specified would be used instead
    of autodetection from filename. Supported formats right now are
    “json”, “yaml” or “mpk”.


    * **\*\*kwargs** – Any of the kwargs supported by json/yaml.load.



* **Returns**

    (object) Result of json/yaml/msgpack.load.