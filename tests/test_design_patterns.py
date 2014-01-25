#!/usr/bin/env python

__author__ = 'Shyue Ping Ong'
__copyright__ = 'Copyright 2014, The Materials Virtual Lab'
__version__ = '0.1'
__maintainer__ = 'Shyue Ping Ong'
__email__ = 'ongsp@ucsd.edu'
__date__ = '1/24/14'


import unittest

from monty.design_patterns import singleton, cached_class


class SingletonTest(unittest.TestCase):

    def test_singleton(self):

        @singleton
        class A():
            pass

        a1 = A()
        a2 = A()

        self.assertEqual(id(a1), id(a2))

class CachedClassTest(unittest.TestCase):

    def test_cached_class(self):

        @cached_class
        class A(object):

            def __init__(self, val):
                self.val = val

        a1a = A(1)
        a1b = A(1)
        a2 = A(2)

        self.assertEqual(id(a1a), id(a1b))
        self.assertNotEqual(id(a1a), id(a2))


if __name__ == "__main__":
    unittest.main()
