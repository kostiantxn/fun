from typing import Any

from fun.monads.monad import Monad


class Maybe(Monad):
    """An optional value.

    The implementation has the following form:

        data Maybe a = Just a | Nothing
    """

    @classmethod
    def unit(cls, x):
        return Just(x)

    @classmethod
    def bind(cls, m, g):
        if isinstance(m, Just):
            return g(m.value)
        if isinstance(m, Nothing):
            return Nothing()


class Just(Maybe):
    """Represents an existing value."""

    def __init__(self, value: Any):
        self._value = value

    def __repr__(self):
        return f'Just({repr(self._value)})'

    def __str__(self):
        return f'Just {self._value}'

    @property
    def value(self) -> Any:
        """Returns the stored value."""
        return self._value


class Nothing(Maybe):
    """Represents an absence of a value."""

    def __repr__(self):
        return 'Nothing()'

    def __str__(self):
        return 'Nothing'
