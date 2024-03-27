"""
Multiprocessing utilities.
"""

from __future__ import annotations

from multiprocessing import Pool
from typing import Callable, Iterable

try:
    from tqdm.autonotebook import tqdm
except ImportError:
    tqdm = None


def imap_tqdm(nprocs: int, func: Callable, iterable: Iterable, *args, **kwargs) -> list:
    """
    A wrapper around Pool.imap. Creates a Pool with nprocs and then runs a f
    unction over an iterable with progress bar.

    Args:
        nprocs: Number of processes
        func: Callable
        iterable: Iterable of arguments.
        args: Passthrough to Pool.imap
        kwargs: Passthrough to Pool.imap

    Returns:
        Results of Pool.imap.
    """
    if tqdm is None:
        raise ImportError("tqdm must be installed for this function.")
    data = []
    with Pool(nprocs) as pool:
        try:
            n = len(iterable)  # type: ignore
        except TypeError:
            n = None  # type: ignore
        with tqdm(total=n) as pbar:
            for d in pool.imap(func, iterable, *args, **kwargs):
                pbar.update()
                data.append(d)
    return data
