import operator
from abc import ABCMeta, abstractmethod
from typing import Any


def as_expression(value: Any) -> 'Expression':
    """Wraps the `value` into an `Expression` object."""

    if isinstance(value, Expression):
        return value
    elif isinstance(value, (int, float, complex, bool, str)):
        return Constant(value)

    raise ValueError(f'Value {repr(value)} cannot be '
                     f'converted to an expression.')


class Expression(metaclass=ABCMeta):
    """Represents an expression that can be evaluated."""

    @abstractmethod
    def eval(self, args):
        """Evaluates the expression depending
        on the provided variables."""

    def __pos__(self) -> 'Expression':
        return Function(operator.pos, self)

    def __neg__(self) -> 'Expression':
        return Function(operator.neg, self)

    def __abs__(self) -> 'Expression':
        return Function(operator.abs, self)

    def __add__(self, other) -> 'Expression':
        return Function(operator.add, self, other)

    def __sub__(self, other) -> 'Expression':
        return Function(operator.sub, self, other)

    def __mul__(self, other) -> 'Expression':
        return Function(operator.mul, self, other)

    def __truediv__(self, other) -> 'Expression':
        return Function(operator.truediv, self, other)

    def __floordiv__(self, other) -> 'Expression':
        return Function(operator.floordiv, self, other)

    def __pow__(self, power, modulo=None) -> 'Expression':
        return Function(operator.pow, self, power, modulo)

    def __radd__(self, other) -> 'Expression':
        return Function(operator.add, other, self)

    def __rsub__(self, other) -> 'Expression':
        return Function(operator.sub, other, self)

    def __rmul__(self, other) -> 'Expression':
        return Function(operator.mul, other, self)

    def __rtruediv__(self, other) -> 'Expression':
        return Function(operator.truediv, other, self)

    def __rfloordiv__(self, other) -> 'Expression':
        return Function(operator.floordiv, other, self)

    def __rpow__(self, other) -> 'Expression':
        return Function(operator.pow, other, self)


class Variable(Expression):
    """An expression that consists of a single variable."""

    def __init__(self, name):
        self.name = name

    def eval(self, args):
        if self.name not in args:
            raise NameError(f"Variable '{self.name}' is not defined.")

        return args[self.name]


class Constant(Expression):
    """An expression of a constant value."""

    def __init__(self, value):
        self._value = value

    def eval(self, args):
        return self._value


class Function(Expression):
    """An expression that applies a function to argument expressions."""

    def __init__(self, f, *x):
        self._f = f
        self._x = list(map(as_expression, x))

    def eval(self, args):
        f = self._f
        x = [x.eval(args) for x in self._x]

        return f(*x)
