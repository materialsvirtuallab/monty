from monty.fnmatch import WildCard


def test_match():
    wc = WildCard("*.pdf")
    assert wc.match("A.pdf")
    assert not wc.match("A.pdg")
