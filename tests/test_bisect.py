from monty.bisect import find_ge, find_gt, find_le, find_lt, index


def test_funcs():
    line = [0, 1, 2, 3, 4]
    assert index(line, 1) == 1
    assert find_lt(line, 1) == 0
    assert find_gt(line, 1) == 2
    assert find_le(line, 1) == 1
    assert find_ge(line, 2) == 2
    # assert index([0, 1, 1.5, 2], 1.501, atol=0.1) == 4
