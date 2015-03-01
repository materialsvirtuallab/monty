"""
functools, especially backported from Python 3.
"""

from __future__ import absolute_import

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2013, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '8/29/14'


from collections import namedtuple
from functools import update_wrapper, wraps, partial


try:
    from threading import RLock
except:
    class RLock:
        """Dummy reentrant lock for builds without threads"""

        def __enter__(self):
            pass

        def __exit__(self, exctype, excinst, exctb):
            pass


_CacheInfo = namedtuple("CacheInfo", ["hits", "misses", "maxsize", "currsize"])


class _HashedSeq(list):
    """
    This class guarantees that hash() will be called no more than once
    per element.  This is important because the lru_cache() will hash
    the key multiple times on a cache miss.
    """

    __slots__ = 'hashvalue'

    def __init__(self, tup, hash=hash):
        self[:] = tup
        self.hashvalue = hash(tup)

    def __hash__(self):
        return self.hashvalue


def _make_key(args, kwds, typed,
              kwd_mark=(object(),),
              fasttypes={int, str, frozenset, type(None)},
              sorted=sorted, tuple=tuple, type=type, len=len):
    """
    Make a cache key from optionally typed positional and keyword arguments

    The key is constructed in a way that is flat as possible rather than
    as a nested structure that would take more memory.

    If there is only a single argument and its data type is known to cache
    its hash value, then that argument is returned without a wrapper.  This
    saves space and improves lookup speed.

    """
    key = args
    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]
    return _HashedSeq(key)


def lru_cache(maxsize=128, typed=False):
    """Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features are disabled and the cache
    can grow without bound.

    If *typed* is True, arguments of different types will be cached separately.
    For example, f(3.0) and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits, misses, maxsize, currsize)
    with f.cache_info().  Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    """

    # Users should only access the lru_cache through its public API:
    #       cache_info, cache_clear, and f.__wrapped__
    # The internals of the lru_cache are encapsulated for thread safety and
    # to allow the implementation to change (including a possible C version).

    # Early detection of an erroneous call to @lru_cache without any arguments
    # resulting in the inner function being passed to maxsize instead of an
    # integer or None.
    if maxsize is not None and not isinstance(maxsize, int):
        raise TypeError('Expected maxsize to be an integer or None')

    # Constants shared by all lru cache instances:
    sentinel = object()          # unique object used to signal cache misses
    make_key = _make_key         # build a key from the function arguments
    PREV, NEXT, KEY, RESULT = 0, 1, 2, 3   # names for the link fields

    def decorating_function(user_function):
        cache = {}
        hits = [0]
        misses = [0]
        full = [False]
        cache_get = cache.get    # bound method to lookup a key or return None
        lock = RLock()           # because linkedlist updates aren't threadsafe
        root = []                # root of the circular doubly linked list
        root[:] = [root, root, None, None]     # initialize by pointing to self
        r = [root]

        if maxsize == 0:

            def wrapper(*args, **kwds):
                # No caching -- just a statistics update after a successful call
                result = user_function(*args, **kwds)
                misses[0] += 1
                return result

        elif maxsize is None:

            def wrapper(*args, **kwds):
                # Simple caching without ordering or size limit
                key = make_key(args, kwds, typed)
                result = cache_get(key, sentinel)
                if result is not sentinel:
                    hits[0] += 1
                    return result
                result = user_function(*args, **kwds)
                cache[key] = result
                misses[0] += 1
                return result

        else:
            def wrapper(*args, **kwds):
                # Size limited caching that tracks accesses by recency
                key = make_key(args, kwds, typed)
                with lock:
                    link = cache_get(key)
                    if link is not None:
                        # Move the link to the front of the circular queue
                        link_prev, link_next, _key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last = r[0][PREV]
                        last[NEXT] = r[0][PREV] = link
                        link[PREV] = last
                        link[NEXT] = r[0]
                        hits[0] += 1
                        return result
                result = user_function(*args, **kwds)
                with lock:
                    if key in cache:
                        # Getting here means that this same key was added to the
                        # cache while the lock was released.  Since the link
                        # update is already done, we need only return the
                        # computed result and update the count of misses.
                        pass
                    elif full[0]:
                        # Use the old root to store the new key and result.
                        oldroot = r[0]
                        oldroot[KEY] = key
                        oldroot[RESULT] = result
                        # Empty the oldest link and make it the new root.
                        # Keep a reference to the old key and old result to
                        # prevent their ref counts from going to zero during the
                        # update. That will prevent potentially arbitrary object
                        # clean-up code (i.e. __del__) from running while we're
                        # still adjusting the links.
                        r[0] = oldroot[NEXT]
                        oldkey = r[0][KEY]
                        oldresult = r[0][RESULT]
                        r[0][KEY] = r[0][RESULT] = None
                        # Now update the cache dictionary.
                        del cache[oldkey]
                        # Save the potentially reentrant cache[key] assignment
                        # for last, after the root and links have been put in
                        # a consistent state.
                        cache[key] = oldroot
                    else:
                        # Put result in a new link at the front of the queue.
                        last = r[0][PREV]
                        link = [last, r[0], key, result]
                        last[NEXT] = r[0][PREV] = cache[key] = link
                        full[0] = (len(cache) >= maxsize)
                    misses[0] += 1
                return result

        def cache_info():
            """Report cache statistics"""
            with lock:
                return _CacheInfo(hits[0], misses[0], maxsize, len(cache))

        def cache_clear():
            """Clear the cache and cache statistics"""
            with lock:
                cache.clear()
                root[:] = [root, root, None, None]
                r[0] = root
                hits[0] = 0
                misses[0] = 0
                full[0] = False

        wrapper.cache_info = cache_info
        wrapper.cache_clear = cache_clear
        return update_wrapper(wrapper, user_function)

    return decorating_function


class lazy_property(object):
    """
    lazy_property descriptor

    Used as a decorator to create lazy attributes. Lazy attributes
    are evaluated on first use.
    """

    def __init__(self, func):
        self.__func = func
        wraps(self.__func)(self)

    def __get__(self, inst, inst_cls):
        if inst is None:
            return self

        if not hasattr(inst, '__dict__'):
            raise AttributeError("'%s' object has no attribute '__dict__'"
                                 % (inst_cls.__name__,))

        name = self.__name__
        if name.startswith('__') and not name.endswith('__'):
            name = '_%s%s' % (inst_cls.__name__, name)

        value = self.__func(inst)
        inst.__dict__[name] = value
        return value

    @classmethod
    def invalidate(cls, inst, name):
        """Invalidate a lazy attribute.

        This obviously violates the lazy contract. A subclass of lazy
        may however have a contract where invalidation is appropriate.
        """
        inst_cls = inst.__class__

        if not hasattr(inst, '__dict__'):
            raise AttributeError("'%s' object has no attribute '__dict__'"
                                 % (inst_cls.__name__,))

        if name.startswith('__') and not name.endswith('__'):
            name = '_%s%s' % (inst_cls.__name__, name)

        if not isinstance(getattr(inst_cls, name), cls):
            raise AttributeError("'%s.%s' is not a %s attribute"
                                 % (inst_cls.__name__, name, cls.__name__))

        if name in inst.__dict__:
            del inst.__dict__[name]


def benchmark(func):
    """
    A decorator that computes the time a function takes to execute
    and stores it in the __etime attribute.
    """
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        etime = time.clock() - t
        #print(func.__name__, etime)
        func.__etime = etime
        return res
    return wrapper


def return_if_raise(exception_tuple, retval_if_exc, disabled=False):
    """
    Decorator for functions, methods or properties. Execute the callable in a
    try block, and return retval_if_exc if one of the exceptions listed in
    exception_tuple is raised (se also ``return_node_if_raise``).

    Setting disabled to True disables the try except block (useful for
    debugging purposes). One can use this decorator to define properties.

    Example::

        @return_if_raise(ValueError, None)
        def return_none_if_value_error(self):
            pass

        @return_if_raise((ValueError, KeyError), "hello")
        def another_method(self):
            pass

        @property
        @return_if_raise(AttributeError, None)
        def name(self):
            "Name of the object, None if not set."
            return self._name

    """
    # we need a tuple of exceptions.
    if isinstance(exception_tuple, list):
        exception_tuple = tuple(exception_tuple)
    elif not isinstance(exception_tuple, tuple):
        exception_tuple = (exception_tuple,)
    else:
        raise TypeError("Wrong exception_tuple %s" % type(exception_tuple))

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if disabled:
                return func(*args, **kwargs)
            try:
                return func(*args, **kwargs)
            except exception_tuple:
                return retval_if_exc
            else:
                raise
        return wrapper
    return decorator


# One could use None as default value in return_if_raise but this one is
# explicit and  more readable
return_none_if_raise = partial(return_if_raise, retval_if_exc=None)
"""
This decorator returns None if one of the exceptions is raised.

    @return_none_if_raise(ValueError)
    def method(self):
"""
