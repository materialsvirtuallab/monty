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


    * [`cd()`](monty.os.md#monty.os.cd)


    * [`makedirs_p()`](monty.os.md#monty.os.makedirs_p)




        * [monty.os.path module](monty.os.path.md)


            * [`find_exts()`](monty.os.path.md#monty.os.path.find_exts)


            * [`zpath()`](monty.os.path.md#monty.os.path.zpath)




* [monty.bisect module](monty.bisect.md)


    * [`find_ge()`](monty.bisect.md#monty.bisect.find_ge)


    * [`find_gt()`](monty.bisect.md#monty.bisect.find_gt)


    * [`find_le()`](monty.bisect.md#monty.bisect.find_le)


    * [`find_lt()`](monty.bisect.md#monty.bisect.find_lt)


    * [`index()`](monty.bisect.md#monty.bisect.index)


* [monty.collections module](monty.collections.md)


    * [`AttrDict`](monty.collections.md#monty.collections.AttrDict)


        * [`AttrDict.copy()`](monty.collections.md#monty.collections.AttrDict.copy)


    * [`FrozenAttrDict`](monty.collections.md#monty.collections.FrozenAttrDict)


    * [`MongoDict`](monty.collections.md#monty.collections.MongoDict)


    * [`Namespace`](monty.collections.md#monty.collections.Namespace)


        * [`Namespace.update()`](monty.collections.md#monty.collections.Namespace.update)


    * [`dict2namedtuple()`](monty.collections.md#monty.collections.dict2namedtuple)


    * [`frozendict`](monty.collections.md#monty.collections.frozendict)


        * [`frozendict.update()`](monty.collections.md#monty.collections.frozendict.update)


    * [`tree()`](monty.collections.md#monty.collections.tree)


* [monty.design_patterns module](monty.design_patterns.md)


    * [`NullFile`](monty.design_patterns.md#monty.design_patterns.NullFile)


    * [`NullStream`](monty.design_patterns.md#monty.design_patterns.NullStream)


        * [`NullStream.write()`](monty.design_patterns.md#monty.design_patterns.NullStream.write)


    * [`cached_class()`](monty.design_patterns.md#monty.design_patterns.cached_class)


    * [`singleton()`](monty.design_patterns.md#monty.design_patterns.singleton)


* [monty.dev module](monty.dev.md)


    * [`deprecated()`](monty.dev.md#monty.dev.deprecated)


    * [`get_ncpus()`](monty.dev.md#monty.dev.get_ncpus)


    * [`install_excepthook()`](monty.dev.md#monty.dev.install_excepthook)


    * [`requires`](monty.dev.md#monty.dev.requires)


* [monty.fnmatch module](monty.fnmatch.md)


    * [`WildCard`](monty.fnmatch.md#monty.fnmatch.WildCard)


        * [`WildCard.filter()`](monty.fnmatch.md#monty.fnmatch.WildCard.filter)


        * [`WildCard.match()`](monty.fnmatch.md#monty.fnmatch.WildCard.match)


* [monty.fractions module](monty.fractions.md)


    * [`gcd()`](monty.fractions.md#monty.fractions.gcd)


    * [`gcd_float()`](monty.fractions.md#monty.fractions.gcd_float)


    * [`lcm()`](monty.fractions.md#monty.fractions.lcm)


* [monty.functools module](monty.functools.md)


    * [`TimeoutError`](monty.functools.md#monty.functools.TimeoutError)


    * [`lazy_property`](monty.functools.md#monty.functools.lazy_property)


        * [`lazy_property.invalidate()`](monty.functools.md#monty.functools.lazy_property.invalidate)


    * [`lru_cache()`](monty.functools.md#monty.functools.lru_cache)


    * [`prof_main()`](monty.functools.md#monty.functools.prof_main)


    * [`return_if_raise()`](monty.functools.md#monty.functools.return_if_raise)


    * [`return_none_if_raise()`](monty.functools.md#monty.functools.return_none_if_raise)


    * [`timeout`](monty.functools.md#monty.functools.timeout)


        * [`timeout.handle_timeout()`](monty.functools.md#monty.functools.timeout.handle_timeout)


* [monty.inspect module](monty.inspect.md)


    * [`all_subclasses()`](monty.inspect.md#monty.inspect.all_subclasses)


    * [`caller_name()`](monty.inspect.md#monty.inspect.caller_name)


    * [`find_top_pyfile()`](monty.inspect.md#monty.inspect.find_top_pyfile)


    * [`initializer()`](monty.inspect.md#monty.inspect.initializer)


* [monty.io module](monty.io.md)


    * [`FileLock`](monty.io.md#monty.io.FileLock)


        * [`FileLock.Error`](monty.io.md#monty.io.FileLock.Error)


        * [`FileLock.acquire()`](monty.io.md#monty.io.FileLock.acquire)


        * [`FileLock.release()`](monty.io.md#monty.io.FileLock.release)


    * [`FileLockException`](monty.io.md#monty.io.FileLockException)


    * [`get_open_fds()`](monty.io.md#monty.io.get_open_fds)


    * [`reverse_readfile()`](monty.io.md#monty.io.reverse_readfile)


    * [`reverse_readline()`](monty.io.md#monty.io.reverse_readline)


    * [`zopen()`](monty.io.md#monty.io.zopen)


* [monty.itertools module](monty.itertools.md)


    * [`chunks()`](monty.itertools.md#monty.itertools.chunks)


    * [`ilotri()`](monty.itertools.md#monty.itertools.ilotri)


    * [`iterator_from_slice()`](monty.itertools.md#monty.itertools.iterator_from_slice)


    * [`iuptri()`](monty.itertools.md#monty.itertools.iuptri)


* [monty.json module](monty.json.md)


    * [`MSONError`](monty.json.md#monty.json.MSONError)


    * [`MSONable`](monty.json.md#monty.json.MSONable)


        * [`MSONable.REDIRECT`](monty.json.md#monty.json.MSONable.REDIRECT)


        * [`MSONable.as_dict()`](monty.json.md#monty.json.MSONable.as_dict)


        * [`MSONable.from_dict()`](monty.json.md#monty.json.MSONable.from_dict)


        * [`MSONable.to_json()`](monty.json.md#monty.json.MSONable.to_json)


        * [`MSONable.unsafe_hash()`](monty.json.md#monty.json.MSONable.unsafe_hash)


        * [`MSONable.validate_monty()`](monty.json.md#monty.json.MSONable.validate_monty)


    * [`MontyDecoder`](monty.json.md#monty.json.MontyDecoder)


        * [`MontyDecoder.decode()`](monty.json.md#monty.json.MontyDecoder.decode)


        * [`MontyDecoder.process_decoded()`](monty.json.md#monty.json.MontyDecoder.process_decoded)


    * [`MontyEncoder`](monty.json.md#monty.json.MontyEncoder)


        * [`MontyEncoder.default()`](monty.json.md#monty.json.MontyEncoder.default)


    * [`jsanitize()`](monty.json.md#monty.json.jsanitize)


* [monty.logging module](monty.logging.md)


    * [`enable_logging()`](monty.logging.md#monty.logging.enable_logging)


    * [`logged()`](monty.logging.md#monty.logging.logged)


* [monty.math module](monty.math.md)


    * [`nCr()`](monty.math.md#monty.math.nCr)


    * [`nPr()`](monty.math.md#monty.math.nPr)


* [monty.msgpack module](monty.msgpack.md)


    * [`default()`](monty.msgpack.md#monty.msgpack.default)


    * [`object_hook()`](monty.msgpack.md#monty.msgpack.object_hook)


* [monty.multiprocessing module](monty.multiprocessing.md)


    * [`imap_tqdm()`](monty.multiprocessing.md#monty.multiprocessing.imap_tqdm)


* [monty.operator module](monty.operator.md)


    * [`operator_from_str()`](monty.operator.md#monty.operator.operator_from_str)


* [monty.pprint module](monty.pprint.md)


    * [`DisplayEcoder`](monty.pprint.md#monty.pprint.DisplayEcoder)


        * [`DisplayEcoder.default()`](monty.pprint.md#monty.pprint.DisplayEcoder.default)


    * [`draw_tree()`](monty.pprint.md#monty.pprint.draw_tree)


    * [`pprint_json()`](monty.pprint.md#monty.pprint.pprint_json)


    * [`pprint_table()`](monty.pprint.md#monty.pprint.pprint_table)


* [monty.re module](monty.re.md)


    * [`regrep()`](monty.re.md#monty.re.regrep)


* [monty.serialization module](monty.serialization.md)


    * [`dumpfn()`](monty.serialization.md#monty.serialization.dumpfn)


    * [`loadfn()`](monty.serialization.md#monty.serialization.loadfn)


* [monty.shutil module](monty.shutil.md)


    * [`compress_dir()`](monty.shutil.md#monty.shutil.compress_dir)


    * [`compress_file()`](monty.shutil.md#monty.shutil.compress_file)


    * [`copy_r()`](monty.shutil.md#monty.shutil.copy_r)


    * [`decompress_dir()`](monty.shutil.md#monty.shutil.decompress_dir)


    * [`decompress_file()`](monty.shutil.md#monty.shutil.decompress_file)


    * [`gzip_dir()`](monty.shutil.md#monty.shutil.gzip_dir)


    * [`remove()`](monty.shutil.md#monty.shutil.remove)


* [monty.string module](monty.string.md)


    * [`boxed()`](monty.string.md#monty.string.boxed)


    * [`indent()`](monty.string.md#monty.string.indent)


    * [`is_string()`](monty.string.md#monty.string.is_string)


    * [`list_strings()`](monty.string.md#monty.string.list_strings)


    * [`make_banner()`](monty.string.md#monty.string.make_banner)


    * [`marquee()`](monty.string.md#monty.string.marquee)


    * [`remove_non_ascii()`](monty.string.md#monty.string.remove_non_ascii)


    * [`unicode2str()`](monty.string.md#monty.string.unicode2str)


* [monty.subprocess module](monty.subprocess.md)


    * [`Command`](monty.subprocess.md#monty.subprocess.Command)


        * [`Command.retcode`](monty.subprocess.md#monty.subprocess.Command.retcode)


        * [`Command.killed`](monty.subprocess.md#monty.subprocess.Command.killed)


        * [`Command.output`](monty.subprocess.md#monty.subprocess.Command.output)


        * [`Command.error`](monty.subprocess.md#monty.subprocess.Command.error)


        * [`Command.run()`](monty.subprocess.md#monty.subprocess.Command.run)


* [monty.tempfile module](monty.tempfile.md)


    * [`ScratchDir`](monty.tempfile.md#monty.tempfile.ScratchDir)


        * [`ScratchDir.SCR_LINK`](monty.tempfile.md#monty.tempfile.ScratchDir.SCR_LINK)


* [monty.termcolor module](monty.termcolor.md)


    * [`colored()`](monty.termcolor.md#monty.termcolor.colored)


    * [`cprint()`](monty.termcolor.md#monty.termcolor.cprint)