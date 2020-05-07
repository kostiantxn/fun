from fluffy.monads import Monad


class Function(Monad):
    """The `Function` data type."""

    def __init__(self, f):
        self._f = f

    def __call__(self, *args, **kwargs):
        return self._f(*args, **kwargs)

    @classmethod
    def unit(cls, x):
        return Function(lambda _: x)

    @classmethod
    def bind(cls, m, g):
        return Function(lambda x: g(m(x))(x))
