from monty.operator import operator_from_str


def test_operator_from_str():
    assert operator_from_str("==")(1, 1) and operator_from_str("+")(1, 1) == 2
