import logging
from io import StringIO

from monty.logging import logged


@logged()
def add(a, b):
    return a + b


def test_logged():
    s = StringIO()
    logging.basicConfig(level=logging.DEBUG, stream=s)
    add(1, 2)
