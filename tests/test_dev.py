import unittest
import warnings

import pytest

from monty.dev import deprecated, install_excepthook, requires


class A:
    @property
    def repl_prop(self):
        pass

    @deprecated(repl_prop)  # type: ignore
    @property
    def prop(self):
        pass


class TestDecorator:
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
            assert issubclass(w[0].category, FutureWarning)
            assert "hello" in str(w[0].message)

    def test_deprecated_property(self):
        class a:
            def __init__(self):
                pass

            @property
            def property_a(self):
                pass

            @property  # type: ignore
            @deprecated(property_a)
            def property_b(self):
                return "b"

            @deprecated(property_a)
            def func_a(self):
                return "a"

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            assert a().property_b == "b"
            # Verify some things
            assert issubclass(w[-1].category, FutureWarning)

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            assert a().func_a() == "a"
            # Verify some things
            assert issubclass(w[-1].category, FutureWarning)

    def test_deprecated_classmethod(self):
        class A:
            def __init__(self):
                pass

            @classmethod
            def classmethod_a(cls):
                pass

            @classmethod
            @deprecated(classmethod_a)
            def classmethod_b(cls):
                return "b"

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            assert A().classmethod_b() == "b"
            # Verify some things
            assert issubclass(w[-1].category, FutureWarning)

        class A:
            def __init__(self):
                pass

            @classmethod
            def classmethod_a(cls):
                pass

            @classmethod
            @deprecated(classmethod_a, category=DeprecationWarning)
            def classmethod_b(cls):
                return "b"

        with pytest.warns(DeprecationWarning):
            assert A().classmethod_b() == "b"

    def test_requires(self):
        try:
            import fictitious_mod  # type: ignore
        except ImportError:
            fictitious_mod = None  # type: ignore

        err_msg = "fictitious_mod is not present."

        @requires(fictitious_mod is not None, err_msg)
        def use_fictitious_mod():
            print("success")

        with pytest.raises(RuntimeError, match=err_msg):
            use_fictitious_mod()

        @requires(unittest is not None, "unittest is not present.")
        def use_unittest():
            return "success"

        assert use_unittest() == "success"

        # test with custom error class
        @requires(False, "expect ImportError", err_cls=ImportError)
        def use_import_error():
            return "success"

        with pytest.raises(ImportError, match="expect ImportError"):
            use_import_error()

    def test_install_except_hook(self):
        install_excepthook()
