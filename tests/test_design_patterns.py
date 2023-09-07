from monty.design_patterns import cached_class, singleton


class TestSingleton:
    def test_singleton(self):
        @singleton
        class A:
            pass

        a1 = A()
        a2 = A()

        assert id(a1) == id(a2)


@cached_class
class A:
    def __init__(self, val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

    def __getinitargs__(self):
        return (self.val,)

    def __getnewargs__(self):
        return (self.val,)


class TestCachedClass:
    def test_cached_class(self):
        a1a = A(1)
        a1b = A(1)
        a2 = A(2)

        assert id(a1a) == id(a1b)
        assert id(a1a) != id(a2)

    # def test_pickle(self):
    #     a = A(2)
    #     o = pickle.dumps(a)
    #     assert a == pickle.loads(o)
