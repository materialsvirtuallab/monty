from __future__ import annotations

import datetime
import unittest
import warnings
from dataclasses import dataclass
from unittest.mock import patch

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
            """This is the old function."""
            pass

        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            func_old()
            # Verify Warning and message
            assert issubclass(w[0].category, FutureWarning)
            assert "Use func_replace instead" in str(w[0].message)

        # Check metadata preservation
        assert func_old.__name__ == "func_old"
        assert func_old.__doc__ == "This is the old function."

    def test_deprecated_str_replacement(self):
        @deprecated("func_replace")
        def func_old():
            pass

        with warnings.catch_warnings(record=True) as w:
            # Trigger a warning.
            func_old()
            # Verify Warning and message
            assert issubclass(w[0].category, FutureWarning)
            assert "use func_replace instead" in str(w[0].message)

    def test_deprecated_property(self):
        class TestClass:
            """A dummy class for tests."""

            @property
            def property_a(self):
                pass

            @property
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

    def test_deprecated_class(self):
        class TestClassNew:
            """A dummy class for tests."""

            def method_a(self):
                pass

        @deprecated(replacement=TestClassNew)
        class TestClassOld:
            """A dummy old class for tests."""

            class_attrib_old = "OLD_ATTRIB"

            def method_b(self):
                """This is method_b."""
                pass

        with pytest.warns(FutureWarning, match="TestClassOld is deprecated"):
            old_class = TestClassOld()

        # Check metadata preservation
        assert old_class.__doc__ == "A dummy old class for tests."
        assert old_class.class_attrib_old == "OLD_ATTRIB"
        assert old_class.__module__ == __name__

        assert old_class.method_b.__doc__ == "This is method_b."

    def test_deprecated_dataclass(self):
        @dataclass
        class TestClassNew:
            """A dummy class for tests."""

            def __post_init__(self):
                print("Hello.")

            def method_a(self):
                pass

        @deprecated(replacement=TestClassNew)
        @dataclass
        class TestClassOld:
            """A dummy old class for tests."""

            class_attrib_old = "OLD_ATTRIB"

            def __post_init__(self):
                print("Hello.")

            def method_b(self):
                """This is method_b."""
                pass

        with pytest.warns(FutureWarning, match="TestClassOld is deprecated"):
            old_class = TestClassOld()

        # Check metadata preservation
        assert old_class.__doc__ == "A dummy old class for tests."
        assert old_class.class_attrib_old == "OLD_ATTRIB"

    def test_deprecated_deadline(self, monkeypatch):
        with pytest.warns(
            DeprecationWarning, match="This function should have been removed"
        ):
            with patch("subprocess.run") as mock_run:
                monkeypatch.setenv("CI", "true")  # mock CI env

                # Mock "GITHUB_REPOSITORY"
                monkeypatch.setenv("GITHUB_REPOSITORY", "TESTOWNER/TESTREPO")
                mock_run.return_value.stdout.decode.return_value = (
                    "git@github.com:TESTOWNER/TESTREPO.git"
                )

                @deprecated(deadline=(2000, 1, 1))
                def func_old():
                    pass

    def test_deprecated_deadline_no_warn(self, monkeypatch):
        """Test cases where no warning should be raised."""

        # No warn case 1: date before deadline
        with warnings.catch_warnings():
            with patch("subprocess.run") as mock_run:
                monkeypatch.setenv("CI", "true")  # mock CI env

                # Mock "GITHUB_REPOSITORY"
                monkeypatch.setenv("GITHUB_REPOSITORY", "TESTOWNER/TESTREPO")
                mock_run.return_value.stdout.decode.return_value = (
                    "git@github.com:TESTOWNER/TESTREPO.git"
                )

                @deprecated(deadline=(9999, 1, 1))
                def func_old():
                    pass

            monkeypatch.undo()

        # No warn case 2: not in CI env
        with warnings.catch_warnings():
            with patch("subprocess.run") as mock_run:
                monkeypatch.delenv("CI", raising=False)

                # Mock "GITHUB_REPOSITORY"
                monkeypatch.setenv("GITHUB_REPOSITORY", "TESTOWNER/TESTREPO")
                mock_run.return_value.stdout.decode.return_value = (
                    "git@github.com:TESTOWNER/TESTREPO.git"
                )

                @deprecated(deadline=(2000, 1, 1))
                def func_old_1():
                    pass

            monkeypatch.undo()

        # No warn case 3: not in code owner repo
        with warnings.catch_warnings():
            monkeypatch.setenv("CI", "true")
            monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)

            @deprecated(deadline=(2000, 1, 1))
            def func_old_2():
                pass

    def test_requires(self):
        try:
            import fictitious_mod
        except ImportError:
            fictitious_mod = None

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
