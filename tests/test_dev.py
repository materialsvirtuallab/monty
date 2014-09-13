__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import warnings
import sys

from monty.dev import deprecated, requires, lazy_property


class A:

    @property
    def repl_prop(self):
        pass

    @deprecated(repl_prop)
    @property
    def prop(self):
        pass


class DecoratorTest(unittest.TestCase):

    def test_deprecated(self):

        def func_a():
            pass

        @deprecated(func_a, "hello")
        def func_b():
            pass

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            func_b()
            # Verify some things
            self.assertTrue(issubclass(w[0].category, DeprecationWarning))
            self.assertIn('hello', str(w[0].message))

    def test_deprecated_property(self):

        class a(object):
            def __init__(self):
                pass

            @property
            def property_a(self):
                pass

            @property
            @deprecated(property_a)
            def property_b(self):
                return 'b'

            @deprecated(property_a)
            def func_a(self):
                return 'a'

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            self.assertEqual(a().property_b, 'b')
            # Verify some things
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            self.assertEqual(a().func_a(), 'a')
            # Verify some things
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))

    def test_requires(self):

        try:
            import fictitious_mod
        except ImportError:
            fictitious_mod = None

        @requires(fictitious_mod is not None, "fictitious_mod is not present.")
        def use_fictitious_mod():
            print("success")

        self.assertRaises(RuntimeError, use_fictitious_mod)

        @requires(unittest is not None, "scipy is not present.")
        def use_unittest():
            return "success"

        self.assertEqual(use_unittest(), "success")


class TestCase(unittest.TestCase):

    def assertException(self, exc_cls, pattern, func, *args, **kw):
        """Assert an exception of type 'exc_cls' is raised and
        'pattern' is contained in the exception message.
        """
        try:
            func(*args, **kw)
        except exc_cls as e:
            exc_str = str(e)
        else:
            self.fail('%s not raised' % (exc_cls.__name__,))

        if pattern not in exc_str:
            self.fail('%r not in %r' % (pattern, exc_str))


class LazyTests(TestCase):

    def test_evaluate(self):
        # Lazy attributes should be evaluated when accessed.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 1)

    def test_evaluate_once(self):
        # lazy_property attributes should be evaluated only once.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(f.foo, 1)
        self.assertEqual(f.foo, 1)
        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 1)

    def test_private_attribute(self):
        # It should be possible to create private, name-mangled
        # lazy_property attributes.
        called = []

        class Foo(object):
            @lazy_property
            def __foo(self):
                called.append('foo')
                return 1
            def get_foo(self):
                return self.__foo

        f = Foo()
        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(len(called), 1)

    def test_reserved_attribute(self):
        # It should be possible to create reserved lazy_property attributes.
        called = []

        class Foo(object):
            @lazy_property
            def __foo__(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(f.__foo__, 1)
        self.assertEqual(f.__foo__, 1)
        self.assertEqual(f.__foo__, 1)
        self.assertEqual(len(called), 1)

    def test_result_shadows_descriptor(self):
        # The result of the function call should be stored in
        # the object __dict__, shadowing the descriptor.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertTrue(isinstance(Foo.foo, lazy_property))
        self.assertTrue(f.foo is f.foo)
        self.assertTrue(f.foo is f.__dict__['foo']) # !
        self.assertEqual(len(called), 1)

        self.assertEqual(f.foo, 1)
        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(f, 'foo')

        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 2)

        self.assertEqual(f.foo, 1)
        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 2)

    def test_readonly_object(self):
        # The descriptor should raise an AttributeError when lazy_property is
        # used on a read-only object (an object with __slots__).
        called = []

        class Foo(object):
            __slots__ = ()
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(len(called), 0)

        self.assertException(AttributeError,
            "'Foo' object has no attribute '__dict__'",
            getattr, f, 'foo')

        # The function was not called
        self.assertEqual(len(called), 0)

    def test_introspection(self):
        # The lazy_property decorator should support basic introspection.

        class Foo(object):
            def foo(self):
                """foo func doc"""
            @lazy_property
            def bar(self):
                """bar func doc"""

        self.assertEqual(Foo.foo.__name__, "foo")
        self.assertEqual(Foo.foo.__doc__, "foo func doc")
        self.assertIn("test_dev", Foo.foo.__module__)

        self.assertEqual(Foo.bar.__name__, "bar")
        self.assertEqual(Foo.bar.__doc__, "bar func doc")
        self.assertIn("test_dev", Foo.bar.__module__)


class InvalidateTests(TestCase):

    def test_invalidate_attribute(self):
        # It should be possible to invalidate a lazy_property attribute.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(f, 'foo')

        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_attribute_twice(self):
        # It should be possible to invalidate a lazy_property attribute
        # twice without causing harm.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(f, 'foo')
        lazy_property.invalidate(f, 'foo') # Nothing happens

        self.assertEqual(f.foo, 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_uncalled_attribute(self):
        # It should be possible to invalidate an empty attribute
        # cache without causing harm.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(len(called), 0)
        lazy_property.invalidate(f, 'foo') # Nothing happens

    def test_invalidate_private_attribute(self):
        # It should be possible to invalidate a private lazy_property attribute.
        called = []

        class Foo(object):
            @lazy_property
            def __foo(self):
                called.append('foo')
                return 1
            def get_foo(self):
                return self.__foo

        f = Foo()
        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(f, '__foo')

        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_mangled_attribute(self):
        # It should be possible to invalidate a private lazy_property attribute
        # by its mangled name.
        called = []

        class Foo(object):
            @lazy_property
            def __foo(self):
                called.append('foo')
                return 1
            def get_foo(self):
                return self.__foo

        f = Foo()
        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(f, '_Foo__foo')

        self.assertEqual(f.get_foo(), 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_reserved_attribute(self):
        # It should be possible to invalidate a reserved lazy_property attribute.
        called = []

        class Foo(object):
            @lazy_property
            def __foo__(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertEqual(f.__foo__, 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(f, '__foo__')

        self.assertEqual(f.__foo__, 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_nonlazy_attribute(self):
        # Invalidating an attribute that is not lazy_property should
        # raise an AttributeError.
        called = []

        class Foo(object):
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertException(AttributeError,
            "'Foo.foo' is not a lazy_property attribute",
            lazy_property.invalidate, f, 'foo')

    def test_invalidate_nonlazy_private_attribute(self):
        # Invalidating a private attribute that is not lazy_property should
        # raise an AttributeError.
        called = []

        class Foo(object):
            def __foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertException(AttributeError,
            "'Foo._Foo__foo' is not a lazy_property attribute",
            lazy_property.invalidate, f, '__foo')

    def test_invalidate_unknown_attribute(self):
        # Invalidating an unknown attribute should
        # raise an AttributeError.
        called = []

        class Foo(object):
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertException(AttributeError,
            "type object 'Foo' has no attribute 'bar'",
            lazy_property.invalidate, f, 'bar')

    def test_invalidate_readonly_object(self):
        # Calling invalidate on a read-only object should
        # raise an AttributeError.
        called = []

        class Foo(object):
            __slots__ = ()
            @lazy_property
            def foo(self):
                called.append('foo')
                return 1

        f = Foo()
        self.assertException(AttributeError,
            "'Foo' object has no attribute '__dict__'",
            lazy_property.invalidate, f, 'foo')


# A lazy_property subclass
class cached(lazy_property):
    pass


class InvalidateSubclassTests(TestCase):

    def test_invalidate_attribute(self):
        # It should be possible to invalidate a cached attribute.
        called = []

        class Bar(object):
            @cached
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertEqual(b.bar, 1)
        self.assertEqual(len(called), 1)

        cached.invalidate(b, 'bar')

        self.assertEqual(b.bar, 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_attribute_twice(self):
        # It should be possible to invalidate a cached attribute
        # twice without causing harm.
        called = []

        class Bar(object):
            @cached
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertEqual(b.bar, 1)
        self.assertEqual(len(called), 1)

        cached.invalidate(b, 'bar')
        cached.invalidate(b, 'bar') # Nothing happens

        self.assertEqual(b.bar, 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_uncalled_attribute(self):
        # It should be possible to invalidate an empty attribute
        # cache without causing harm.
        called = []

        class Bar(object):
            @cached
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertEqual(len(called), 0)
        cached.invalidate(b, 'bar') # Nothing happens

    def test_invalidate_private_attribute(self):
        # It should be possible to invalidate a private cached attribute.
        called = []

        class Bar(object):
            @cached
            def __bar(self):
                called.append('bar')
                return 1
            def get_bar(self):
                return self.__bar

        b = Bar()
        self.assertEqual(b.get_bar(), 1)
        self.assertEqual(len(called), 1)

        cached.invalidate(b, '__bar')

        self.assertEqual(b.get_bar(), 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_mangled_attribute(self):
        # It should be possible to invalidate a private cached attribute
        # by its mangled name.
        called = []

        class Bar(object):
            @cached
            def __bar(self):
                called.append('bar')
                return 1
            def get_bar(self):
                return self.__bar

        b = Bar()
        self.assertEqual(b.get_bar(), 1)
        self.assertEqual(len(called), 1)

        cached.invalidate(b, '_Bar__bar')

        self.assertEqual(b.get_bar(), 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_reserved_attribute(self):
        # It should be possible to invalidate a reserved cached attribute.
        called = []

        class Bar(object):
            @cached
            def __bar__(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertEqual(b.__bar__, 1)
        self.assertEqual(len(called), 1)

        cached.invalidate(b, '__bar__')

        self.assertEqual(b.__bar__, 1)
        self.assertEqual(len(called), 2)

    def test_invalidate_uncached_attribute(self):
        # Invalidating an attribute that is not cached should
        # raise an AttributeError.
        called = []

        class Bar(object):
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertException(AttributeError,
            "'Bar.bar' is not a cached attribute",
            cached.invalidate, b, 'bar')

    def test_invalidate_uncached_private_attribute(self):
        # Invalidating a private attribute that is not cached should
        # raise an AttributeError.
        called = []

        class Bar(object):
            def __bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertException(AttributeError,
            "'Bar._Bar__bar' is not a cached attribute",
            cached.invalidate, b, '__bar')

    def test_invalidate_unknown_attribute(self):
        # Invalidating an unknown attribute should
        # raise an AttributeError.
        called = []

        class Bar(object):
            @cached
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertException(AttributeError,
            "type object 'Bar' has no attribute 'baz'",
            lazy_property.invalidate, b, 'baz')

    def test_invalidate_readonly_object(self):
        # Calling invalidate on a read-only object should
        # raise an AttributeError.
        called = []

        class Bar(object):
            __slots__ = ()
            @cached
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertException(AttributeError,
            "'Bar' object has no attribute '__dict__'",
            cached.invalidate, b, 'bar')

    def test_invalidate_superclass_attribute(self):
        # cached.invalidate CANNOT invalidate a superclass (lazy_property) attribute.
        called = []

        class Bar(object):
            @lazy_property
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertException(AttributeError,
            "'Bar.bar' is not a cached attribute",
            cached.invalidate, b, 'bar')

    def test_invalidate_subclass_attribute(self):
        # Whereas lazy_property.invalidate CAN invalidate a subclass (cached) attribute.
        called = []

        class Bar(object):
            @cached
            def bar(self):
                called.append('bar')
                return 1

        b = Bar()
        self.assertEqual(b.bar, 1)
        self.assertEqual(len(called), 1)

        lazy_property.invalidate(b, 'bar')

        self.assertEqual(b.bar, 1)
        self.assertEqual(len(called), 2)


class AssertExceptionTests(TestCase):

    def test_assert_AttributeError(self):
        self.assertException(AttributeError,
            "'AssertExceptionTests' object has no attribute 'foobar'",
            getattr, self, 'foobar')

    def test_assert_IOError(self):
        self.assertException(IOError,
            "No such file or directory",
            open, './foo/bar/baz/peng/quux', 'rb')

    def test_assert_SystemExit(self):
        self.assertException(SystemExit,
            "",
            sys.exit)

    def test_assert_exception_not_raised(self):
        self.assertRaises(AssertionError,
            self.assertException, AttributeError,
            "'AssertExceptionTests' object has no attribute 'run'",
            getattr, self, 'run')

    def test_assert_pattern_mismatch(self):
        self.assertRaises(AssertionError,
            self.assertException, AttributeError,
            "baz",
            getattr, self, 'foobar')




if __name__ == "__main__":
    unittest.main()