Change log
==========

v2022.3.12
----------
* Allow recursive MSON in jsanitize (@arosen93)
* Option to use orjson for faster decoding. (@munrojm)

v2022.1.19
----------
* Fix ruamel.yaml backwards compatibility.

v2022.1.12
----------
* Fix decoding of dictionaries (@arosen93).
* Formal support for py3.10

v2021.12.1
----------
* Adds support for lzma/xz format in zopen (@zhubonan).

v2021.8.17
----------
* Support serialization for Pandas DataFrames (@mkhorton).

v2021.7.8
---------
* Support the specification of `fmt` keyword arg in monty.serialization
  loadfn and dumpfn.

v2021.6.10
----------
* Expanded support for built-in functions, numpy types, etc. in MSON serialization (@utf).

v2021.5.9
---------
* Drop py3.5 support.

v2021.3.3
---------
* pydantic support (@shyamd)
* UUID serialization support (@utf)

v4.0.2
------
1. Allow specification of warning category in deprecated wrapper.

v4.0.1
------
1. USe FutureWarning in the monty.dev.deprecated wrapper instead.

v3.0.4
------
1. Add support for complex dtypes in MSONable numpy arrays. (@fracci)

v3.0.3
------
1. Improvements to MSONAble to support Varidac Args (@shyamd).

v3.0.1
------
1. Bug fixes for Windows.

v3.0.0
------
1. Py3 only version.

v2.0.7
------
1. MSONable now supports Enum types. (@mkhorton)

v2.0.6
------
1. Revert py27 incompatible fmt spec for loadfn and dumpfn for now. This is
   a much less common use case.

v2.0.5
------
1. Checking for extension type in loadfn and dumpfn now relies on ".json",
   ".yaml" or ".mpk". Further, now ".yml" and ".yaml" are both recognized as
   YAML files. (@clegaspi)
2. A fmt kwarg is now supported in loadfn and dumpfn to specify the format
   explicitly. (@clegaspi)

v2.0.4
------
1. Bug fix for invert MSON caused by `@version`.

v2.0.3
------
1. Support for nested MSONAble objects with MontyEncoder and dumpfn.
   (@davidwaroquiers)
2. Add @version to MSONAble. (@mkhorton)

v2.0.0
------
1. Support for Path object in zopen.

v1.0.5
------
1. Bug fix for io.reverse_readfile to ensure txt or binary string.

v1.0.4
------
1. monty.shutil.remove which allows symlinks removal. Also improved
   monty.tempfile.ScratchDir cleanup. (@shyamd)

v1.0.3
------
1. Bug fix for reverse_readfile for bz2 files (Alex Urban)

v1.0.2
------
1. Misc bug fixes (tempdir on Windows)

v1.0.1
------
1. Use CLoader and CDumper by default for speed.

v1.0.0
------
1. Ruamel.yaml is now used as the default YAML parser and dumper.

v0.9.8
------
1. Now ScratchDir functions as it should by replacing the original directory.

v0.9.7
------
1. Minor update for inspect deprecation.

v0.9.6
------
1. Allow private variable names (with leading underscores) to be auto-detected
   in default MSONable.

v0.9.5
------
1. Favor use of inspect.signature in MSONAble.

v0.9.3
------
1. Fix monty decoding of bson only if bson is present.

v0.9.2
------
1. Minor update.

v0.9.1
------
1. bson.objectid.ObjectId support for MontyEncoder and MontyDecoder.

v0.9.0
------
1. Improved default as and from_dict.

v0.8.5
------
1. Minor bug fixes.

v0.8.4
------
1. Support for bson fields in jsanitize.

v0.8.2
------
1. Fasetr gzip.

v0.8.1
------
1. Update gcd for deprecated fractions.gcd in py >= 3.5. Try math.gcd by default first.

v0.8.0
------
1. A new collections.tree object, which allows nested defaultdicts.

v0.7.2
------
1. Added support for msgpack serialization in monty.serialization.dumpfn, loadfn
   and monty.msgpack.default and object_hook.

v0.7.1
------
1. Added timeout function. Useful to limit function calls that take too long.

v0.7.0
------
1. New backwards incompatible MSONable implementation that inspects init args
   to create a default dict representation for objects.

v0.6.1
------
1. New jsanitize method to convert objects supporting the MSONable protocol
   to json serializable dicts.

v0.6.0
------
1. New frozendict and MongoDict (allows for Javascript like access of nested
   dicts) classes (Matteo).
2. New Command class in subprocess which allows commands to be run in separate
   thread with timeout (Matteo).

v0.5.9
------
1. More fixes for reverse read of gzipped files ofr Py3k.

v0.5.8
------
1. Fix reverse read file for gzipped files.

v0.5.7
------
1. Added a reverse_readfile method in monty.io, which is faster than
   reverse_readline for large files.

v0.5.6
------
1. Provide way to specify Dumper and Loader in monty.serialization.
2. Better handling of unicode.

v0.5.5
------
1. More robust handling of numpy arrays and datetime objects in json.
2. Refactor NotOverwritableDict to Namespace (Matteo).

v0.5.4
------
1. Addition of many help functions in string, itertools, etc. (Matteo).
2. NullFile and NullStream in monty.design_patterns (Matteo).
3. FileLock in monty.io (Matteo)

v0.5.3
------
1. Minor efficiency improvement.

v0.5.2
------
1. Add unicode2str and str2unicode in monty.string.

v0.5.0
------
1. Completely rewritten zopen which supports the "rt" keyword of Python 3
   even when used in Python 2.
2. monty.string now has a marquee method which centers a string
   (contributed by Matteo).
3. Monty now supports only Python >= 3.3 as well as Python 2.7. Python 3.2
   support is now dropped.

v0.4.4
------
1. Refactor lazy_property to be in functools module.

v0.4.3
------
1. Additional dev decorators lazy and logging functions.

v0.4.2
------
1. Improve numpy array serialization with MontyEncoder.

v0.4.1
------
1. Minor bug fix for module load in Py3k.

v0.4.0
------
1. Remove deprecated json.loadf methods.
2. Add MSONable protocol for json/yaml based serialization.
3. deprecated now supports an additonal message.

v0.3.6
------
1. :class:`monty.tempfile.ScratchDir` now checks for existence of root
   directory. If root path does not exist, will function as simple
   pass through. Makes it a lot more robust to bad mounting of scratch
   directories.

v0.3.5
------
1. Added backport of functools.lru_cache.

v0.3.4
------
1. Specialized json encoders / decoders with support for numpy arrays and
   objects supporting a to_dict() protocol used in pymatgen.

v0.3.1
------
1. Proper support for libyaml auto-detect in yaml support.

v0.3.0
------
1. Refactor serialization tools to shorten method names.

v0.2.4
------
1. Added serialization module that supports both json and yaml. The latter
   requires pyyaml.

v0.2.3
------
1. Added get_ncpus method in dev. (G. Matteo).

v0.2.2
------
1. Add a Fabric-inspired cd context manager in monty.os.
2. Refactor ScratchDir context manager to monty.tempfile.

v0.2.1
------
1. Add string module, which provides a function to remove non-ascii
   characters. More to be added.

v0.2.0
------
1. ScratchDir now supports non-copying of files to and from current
   directory, and this is the default (different from prior releases).
2. Yet more improvements to copy_r to prevent recursive infinite loops in
   copying.

v0.1.5
------
1. Added the useful monty.shutil.compress_file, compress_dir,
   decompress_file and decompress_dir methods.
2. Much more robust copy_r in shutil.

v0.1.4
------
1. Bug fix for 0.1.3.

v0.1.2
------
1. Added zpath method to return zipped paths.

v0.1.1
------
1. Minor release to update description.

v0.1.0
------
1. Ensure Python 3+ compatibility.
2. Travis testing implemented.

v0.0.5
------
1. First official alpha release with unittests and docs.

v0.0.2
------
1. Added several decorators and utilities.

v0.0.1
------

1. Initial version.
