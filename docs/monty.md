---
layout: default
title: API Documentation
nav_order: 5
---

# monty package

Monty is the missing complement to Python. Monty implements supplementary
useful functions for Python that are not part of the standard library.
Examples include useful utilities like transparent support for zipped files,
useful design patterns such as singleton and cached_class, and many more.

## Subpackages


* [monty.os package](monty.os.md)


    * `cd()`


    * `makedirs_p()`


        * [monty.os.path module](monty.os.path.md)


            * `find_exts()`


            * `zpath()`


* [monty.bisect module](monty.bisect.md)


    * `find_ge()`


    * `find_gt()`


    * `find_le()`


    * `find_lt()`


    * `index()`


* [monty.collections module](monty.collections.md)


    * `AttrDict`


        * `AttrDict.copy()`


    * `FrozenAttrDict`


    * `MongoDict`


    * `Namespace`


        * `Namespace.update()`


    * `dict2namedtuple()`


    * `frozendict`


        * `frozendict.update()`


    * `tree()`


* [monty.design_patterns module](monty.design_patterns.md)


    * `NullFile`


    * `NullStream`


        * `NullStream.write()`


    * `cached_class()`


    * `singleton()`


* [monty.dev module](monty.dev.md)


    * `deprecated()`


    * `get_ncpus()`


    * `install_excepthook()`


    * `requires`


* [monty.fnmatch module](monty.fnmatch.md)


    * `WildCard`


        * `WildCard.filter()`


        * `WildCard.match()`


* [monty.fractions module](monty.fractions.md)


    * `gcd()`


    * `gcd_float()`


    * `lcm()`


* [monty.functools module](monty.functools.md)


    * `TimeoutError`


    * `lazy_property`


        * `lazy_property.invalidate()`


    * `lru_cache()`


    * `prof_main()`


    * `return_if_raise()`


    * `return_none_if_raise()`


    * `timeout`


        * `timeout.handle_timeout()`


* [monty.inspect module](monty.inspect.md)


    * `all_subclasses()`


    * `caller_name()`


    * `find_top_pyfile()`


* [monty.io module](monty.io.md)


    * `FileLock`


        * `FileLock.Error`


        * `FileLock.acquire()`


        * `FileLock.release()`


    * `FileLockException`


    * `get_open_fds()`


    * `reverse_readfile()`


    * `reverse_readline()`


    * `zopen()`


* [monty.itertools module](monty.itertools.md)


    * `chunks()`


    * `ilotri()`


    * `iterator_from_slice()`


    * `iuptri()`


* [monty.json module](monty.json.md)


    * `MSONError`


    * `MSONable`


        * `MSONable.REDIRECT`


        * `MSONable.as_dict()`


        * `MSONable.from_dict()`


        * `MSONable.to_json()`


        * `MSONable.unsafe_hash()`


        * `MSONable.validate_monty()`


    * `MontyDecoder`


        * `MontyDecoder.decode()`


        * `MontyDecoder.process_decoded()`


    * `MontyEncoder`


        * `MontyEncoder.default()`


    * `jsanitize()`


* [monty.logging module](monty.logging.md)


    * `enable_logging()`


    * `logged()`


* [monty.math module](monty.math.md)


    * `nCr()`


    * `nPr()`


* [monty.msgpack module](monty.msgpack.md)


    * `default()`


    * `object_hook()`


* [monty.multiprocessing module](monty.multiprocessing.md)


    * `imap_tqdm()`


* [monty.operator module](monty.operator.md)


    * `operator_from_str()`


* [monty.pprint module](monty.pprint.md)


    * `DisplayEcoder`


        * `DisplayEcoder.default()`


    * `draw_tree()`


    * `pprint_json()`


    * `pprint_table()`


* [monty.re module](monty.re.md)


    * `regrep()`


* [monty.serialization module](monty.serialization.md)


    * `dumpfn()`


    * `loadfn()`


* [monty.shutil module](monty.shutil.md)


    * `compress_dir()`


    * `compress_file()`


    * `copy_r()`


    * `decompress_dir()`


    * `decompress_file()`


    * `gzip_dir()`


    * `remove()`


* [monty.string module](monty.string.md)


    * `boxed()`


    * `indent()`


    * `is_string()`


    * `list_strings()`


    * `make_banner()`


    * `marquee()`


    * `remove_non_ascii()`


    * `unicode2str()`


* [monty.subprocess module](monty.subprocess.md)


    * `Command`


        * `Command.retcode`


        * `Command.killed`


        * `Command.output`


        * `Command.error`


        * `Command.run()`


* [monty.tempfile module](monty.tempfile.md)


    * `ScratchDir`


        * `ScratchDir.SCR_LINK`


* [monty.termcolor module](monty.termcolor.md)


    * `colored()`


    * `cprint()`