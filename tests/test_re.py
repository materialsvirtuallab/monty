import os

from monty.re import regrep

test_dir = os.path.join(os.path.dirname(__file__), "test_files")


def test_regrep():
    """
    We are making sure a file containing line numbers is read in reverse
    order, i.e. the first line that is read corresponds to the last line.
    number
    """
    fname = os.path.join(test_dir, "3000_lines.txt")
    matches = regrep(fname, {"1": r"1(\d+)", "3": r"3(\d+)"}, postprocess=int)
    assert len(matches["1"]) == 1380
    assert len(matches["3"]) == 571
    assert matches["1"][0][0][0] == 0

    matches = regrep(
        fname,
        {"1": r"1(\d+)", "3": r"3(\d+)"},
        reverse=True,
        terminate_on_match=True,
        postprocess=int,
    )
    assert len(matches["1"]) == 1
    assert len(matches["3"]) == 11
