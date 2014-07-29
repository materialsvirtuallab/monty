#!/usr/bin/env python

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest
import warnings

from monty.dev import deprecated, requires


class DecoratorTest(unittest.TestCase):

    def test_deprecated(self):

        def func_a():
            pass

        @deprecated(func_a)
        def func_b():
            pass

        with warnings.catch_warnings(record=True) as w:
            # Cause all warnings to always be triggered.
            warnings.simplefilter("always")
            # Trigger a warning.
            func_b()
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


if __name__ == "__main__":
    unittest.main()