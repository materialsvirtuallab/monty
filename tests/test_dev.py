import unittest
import warnings
import datetime

import pytest
from monty.dev import deprecated, install_excepthook, requires

# Set all warnings to always be triggered.
warnings.simplefilter("always")


class TestDecorator:
    def test_deprecated(self):
        def func_replace():
            pass

        @deprecated(func_replace, "Use func_replace instead")
        def func_old():
            pass

        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            func_old()
            # Verify Warning and message
            assert issubclass(w[0].category, FutureWarning)
            assert "Use func_replace instead" in str(w[0].message)

    def test_deprecated_property(self):
        class TestClass:
            """A dummy class for tests."""

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
            # Trigger a warning.
            assert TestClass().property_b == "b"
            # Verify warning type
            assert issubclass(w[-1].category, FutureWarning)

        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            assert TestClass().func_a() == "a"
            # Verify some things
            assert issubclass(w[-1].category, FutureWarning)

    def test_deprecated_classmethod(self):
        class TestClass:
            """A dummy class for tests."""

            @classmethod
            def classmethod_a(cls):
                pass

            @classmethod
            @deprecated(classmethod_a)
            def classmethod_b(cls):
                return "b"

        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            assert TestClass().classmethod_b() == "b"
            # Verify some things
            assert issubclass(w[-1].category, FutureWarning)

        class TestClass_deprecationwarning:
            """A dummy class for tests."""

            @classmethod
            def classmethod_a(cls):
                pass

            @classmethod
            @deprecated(classmethod_a, category=DeprecationWarning)
            def classmethod_b(cls):
                return "b"

        with pytest.warns(DeprecationWarning):
            assert TestClass_deprecationwarning().classmethod_b() == "b"

    def test_deprecated_deadline(self):
        @deprecated(deadline=(2000, 1, 1))
        def func_old():
            pass

        with warnings.catch_warnings(record=True) as warn_msgs:
            func_old()  # trigger a warning

            assert "will be removed on 2000-01-01" in str(warn_msgs[0].message)

    def test_deprecated_deadline_no_warn(self, monkeypatch):
        """Test cases where no warning should be raised."""

        @deprecated(deadline=(2000, 1, 1))
        def func_old():
            pass

        # No warn case 1: date before deadline
        with warnings.catch_warnings(record=True) as warn_msgs:
            monkeypatch.setattr(datetime, "datetime", datetime.datetime(1999, 1, 1))
            func_old()

            for warning in warn_msgs:
                assert "This function should have been removed on" not in str(
                    warning.message
                )

        # No warn case 2: not in CI env
        with warnings.catch_warnings(record=True) as warn_msgs:
            monkeypatch.delenv("CI", raising=False)
            func_old()

            for warning in warn_msgs:
                assert "This function should have been removed on" not in str(
                    warning.message
                )

        # No warn case 3: not in code owner repo
        with warnings.catch_warnings(record=True) as warn_msgs:
            monkeypatch.setenv("GITHUB_REPOSITORY", "NONE/NONE")
            func_old()

            for warning in warn_msgs:
                assert "This function should have been removed on" not in str(
                    warning.message
                )

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
