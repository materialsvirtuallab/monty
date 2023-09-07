from math import sqrt

from monty.multiprocessing import imap_tqdm


def test_imap_tqdm():
    results = imap_tqdm(4, sqrt, range(10000))
    assert len(results) == 10000
    assert results[0] == 0
    assert results[400] == 20
    assert results[9999] == 99.99499987499375
    results = imap_tqdm(4, sqrt, (i**2 for i in range(10000)))
    assert len(results) == 10000
    assert results[0] == 0
    assert results[400] == 400
