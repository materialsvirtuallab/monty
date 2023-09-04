---
layout: default
title: monty.multiprocessing.md
nav_exclude: true
---

# monty.multiprocessing module

Multiprocessing utilities.


### monty.multiprocessing.imap_tqdm(nprocs: int, func: Callable, iterable: Iterable, \*args, \*\*kwargs)
A wrapper around Pool.imap. Creates a Pool with nprocs and then runs a f
unction over an iterable with progress bar.


* **Parameters**


    * **nprocs** – Number of processes


    * **func** – Callable


    * **iterable** – Iterable of arguments.


    * **args** – Passthrough to Pool.imap


    * **kwargs** – Passthrough to Pool.imap



* **Returns**

    Results of Pool.imap.