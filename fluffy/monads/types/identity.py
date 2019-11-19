from fluffy.monads.monad import Monad


class Identity(Monad):
    """The `Identity` data type.

    The implementation has the following form:

        data Identity a = Identity a
    """

    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        """Returns the value stored in the `Identity` container."""
        return self._value

    @classmethod
    def bind(cls, m, g):
        return g(m.value)

    @classmethod
    def unit(cls, x):
        return Identity(x)
