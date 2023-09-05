import logging
from io import StringIO

from monty.logging import logged


@logged()
def add(a, b):
    return a + b


class TestFunc:
    def test_logged(self):
        s = StringIO()
        logging.basicConfig(level=logging.DEBUG, stream=s)
        add(1, 2)
