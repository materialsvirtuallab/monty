from monty.fnmatch import WildCard


class TestFunc:
    def test_match(self):
        wc = WildCard("*.pdf")
        assert wc.match("A.pdf")
        assert not wc.match("A.pdg")
