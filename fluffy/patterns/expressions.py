import operator
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union

from fluffy.patterns.errors import EvaluationError


def as_expression(value: Any) -> 'Expression':
    """Creates an instance of `Expression` from the specified value.

    Args:
        value: A value to create an instance of `Expression` from.

    Returns:
        An instance of `Expression` that was constructed depending on
        the specified value.

    Examples:
        >>> as_expression(42)
        Constant(value=42)

        >>> as_expression([451, 1984])
        Sequence(value=[451, 1984])

    Raises:
        TypeError: Raised when the type of the specified value is not
            supported and an instance of `Expression` cannot be created.
    """

    if isinstance(value, Expression):
        return value
    elif isinstance(value, (int, float, complex, bool, str)):
        return Constant(value)
    elif isinstance(value, (list, tuple)):
        return Sequence(value)
    elif isinstance(value, dict):
        return Dictionary(value)

    raise ValueError(f'{value} cannot be converted to an expression.')


class Expression(metaclass=ABCMeta):
    """Represents an expression that can be evaluated."""

    @abstractmethod
    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluates the expression depending on the provided variables.

        Args:
            variables: A dictionary that maps the names of the variables to
                the values of those variables.

        Returns:
            The evaluated value.
        """

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


class Function(Expression):
    """An expression that applies a function to the argument expressions."""

    def __init__(self, f, *x):
        self._f = f
        self._x = list(map(as_expression, x))

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        f = self._f
        x = [x.evaluate(variables) for x in self._x]

        return f(*x)


class Variable(Expression):
    """An expression that consists of a single variable."""

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __repr__(self):
        return f'Variable(name={repr(self.name)})'

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        if self.name not in variables:
            raise NameError(f"Variable '{self.name}' is not defined.")

        return variables[self.name]


class Constant(Expression):
    """An expression that represents a constant value."""

    def __init__(self, value):
        self._value = value

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        return self._value


class Sequence(Expression):
    """..."""

    def __init__(self, value: Union[list, tuple]):
        self._value = value

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        raise NotImplemented


class Dictionary(Expression):
    """..."""

    def __init__(self, value: dict):
        self._value = value

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        raise NotImplemented


class Error(Expression):
    """An expression that raises an error."""

    def __init__(self, value):
        self._value = value

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        if isinstance(self._value, Exception):
            raise self._value
        else:
            raise EvaluationError(self._value)
