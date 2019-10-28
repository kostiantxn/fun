import operator
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Union, Callable

from fluffy.patterns.errors import EvaluationError


def expression(value: Any) -> 'Expression':
    """Creates an instance of `Expression` from the specified value.

    Args:
        value: A value to create an instance of `Expression` from.

    Returns:
        An instance of `Expression` that was constructed depending on
        the specified value.

    Examples:
        >>> expression(42)
        Constant(value=42)

        >>> expression([451, 1984])
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

    raise TypeError(f'{value} cannot be converted to an expression.')


class Expression(metaclass=ABCMeta):
    """An expression that can be evaluated.

    Represents an expression that can be evaluated depending on a dictionary
    of variables.

    Defines operators to add, subtract, multiply, divide, compare expressions
    (the list of operators is not exhaustive).
    """

    @abstractmethod
    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluates the expression depending on the provided variables.

        Args:
            variables: A dictionary that maps the names of the variables to
                the values of those variables.

        Returns:
            The evaluated value.
        """

    def __getattr__(self, item) -> 'Expression':
        return Attribute(self, item)

    def __call__(self, *args, **kwargs) -> 'Expression':
        return Call(self, args, kwargs)

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

    def __mod__(self, other) -> 'Expression':
        return Function(operator.mod, self, other)

    def __pow__(self, power, modulo=None) -> 'Expression':
        return Function(operator.pow, self, power, modulo)

    def __matmul__(self, other) -> 'Expression':
        return Function(operator.matmul, self, other)

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

    def __rmod__(self, other) -> 'Expression':
        return Function(operator.mod, other, self)

    def __rpow__(self, other) -> 'Expression':
        return Function(operator.pow, other, self)

    def __rmatmul__(self, other) -> 'Expression':
        return Function(operator.matmul, other, self)

    def __eq__(self, other) -> 'Expression':
        return Function(operator.eq, self, other)

    def __ne__(self, other) -> 'Expression':
        return Function(operator.ne, self, other)

    def __lt__(self, other) -> 'Expression':
        return Function(operator.lt, self, other)

    def __le__(self, other) -> 'Expression':
        return Function(operator.le, self, other)

    def __gt__(self, other) -> 'Expression':
        return Function(operator.gt, self, other)

    def __ge__(self, other) -> 'Expression':
        return Function(operator.ge, self, other)


class Constant(Expression):
    """An expression representing a constant value.

    Example:
        >>> expr = Constant(42)
        >>> expr.evaluate({})
        42
    """

    def __init__(self, value):
        """Initialises the object.

        Initialises the object with the value that will be returned during the
        evaluation of the expression.

        Args:
            value: Any object that will be returned during the evaluation.
        """

        self.value = value

    def __repr__(self):
        return f'Constant(value={repr(self.value)})'

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Returns the value that the object was initialised with."""
        return self.value


class Variable(Expression):
    """An expression representing a single variable.

    Attributes:
        name (str): The name of the variable.

    Examples:
        >>> expr = Variable('x')
        >>> expr.evaluate({'x': 1, 'y': 2})
        1
    """

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'Variable(name={repr(self.name)})'

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluates the variable.

        Looks up for a value by the name of the variable in the provided
        dictionary of variables.

        Raises:
            NameError: Raised when the name of the variable is not present
                as a key in the dictionary of variables.
        """

        if self.name is None:
            raise ValueError(f"The variable cannot be evaluated.")
        if self.name not in variables:
            raise NameError(f"The variable '{self.name}' is not defined.")

        return variables[self.name]


class Function(Expression):
    """An expression that applies a function to the argument expressions.

    Examples:
        >>> x = Variable('x')

        >>> expr = Function(pow, x, 2)
        >>> expr.evaluate({'x': 2})
        4
        >>> expr.evaluate({'x': 3})
        9
        >>> expr.evaluate({})
        Traceback (most recent call last):
            ...
        NameError: The variable 'x' is not defined.
    """

    def __init__(self, f: Callable, *x: Any):
        """Initialises the object.

        Initialises the object with a function to apply and a list of arguments
        to pass to the function during the evaluation.

        Args:
            f (callable): A function to apply.
            x (iterable): A list of arguments that can be converted to
                instances of `Expression` (i.e. by calling `expression`).
        """

        self._f = f
        self._x = x

    def __repr__(self):
        return f'Function(' \
                   f'{repr(self._f)}, ' \
                   f'{", ".join(map(repr, self._x))}' \
               f')'

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluates each argument and then calls the function."""

        f = self._f
        x = [expression(x).evaluate(variables) for x in self._x]

        return f(*x)


class Sequence(Expression):
    """An expression that represents a sequence (list, tuple).

    Attributes:
        value: A list or tuples of expressions to evaluate.

    Examples:
        >>> x, y = Variable('x'), Variable('y')

        >>> expr = Sequence([1, x, y, 4])
        >>> expr.evaluate({'x': 2, 'y': 3})
        [1, 2, 3, 4]
    """

    def __init__(self, value: Union[list, tuple]):
        self.value = value

    def __repr__(self):
        return f'Sequence(value={repr(self.value)})'

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Returns a sequence with evaluated elements."""

        f = type(self.value)  # Either a `list` or a `tuple`.
        x = (expression(x).evaluate(variables) for x in self.value)

        return f(x)


class Dictionary(Expression):
    """An expression that represents a dictionary.

    Attributes:
        value: A dictionary of expressions to evaluate.

    Examples:
        >>> x, y = Variable('x'), Variable('y')

        >>> expr = Dictionary({1: x, y: 4})
        >>> expr.evaluate({'x': 2, 'y': 3})
        {1: 2, 3: 4}
    """

    def __init__(self, value: dict):
        self.value = value

    def __repr__(self):
        return f'Dictionary(value={repr(self.value)})'

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Returns a dictionary with evaluated elements."""
        return {expression(x).evaluate(variables):
                expression(y).evaluate(variables)
                for x, y in self.value.items()}


class Attribute(Expression):
    """An expression that gets an attribute.

    Attribute:
        expr (Expression): An expression to get an attribute of.
        name (str): The name of an attribute to get.

    Examples:
        >>> from dataclasses import dataclass

        >>> @dataclass
        ... class Person:
        ...     name: str

        >>> expr = Variable('x')
        >>> expr = Attribute(expr, 'name')
        >>> expr.evaluate({'x': Person(name='Richard')})
        'Richard'
    """

    def __init__(self, expr: Expression, name: str):
        self.expr = expr
        self.name = name

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluates the expression and gets its attribute."""
        return getattr(self.expr.evaluate(variables), self.name)


class Call(Expression):
    """A calling expression.

    Attributes:
        expr (Expression): An expression to call.
        *args: Positional arguments to call with.
        **kwargs: Keyword arguments to call with.

    Examples:
        >>> expr = Constant('ABC')
        >>> expr = expr.lower().strip('c')
        >>> expr.evaluate({})
        'ab'
    """

    def __init__(self, expr: Expression, args, kwargs):
        self.expr = expr
        self.args = args
        self.kwargs = kwargs

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Evaluates the expression and calls it."""
        return self.expr.evaluate(variables)(*self.args, **self.kwargs)


class Error(Expression):
    """An expression that raises an error."""

    def __init__(self, value: Union[str, Exception]):
        """Initialises the object with either an error message or an exception.

         Args:
             value: Either an error message or an instance of `Exception`.
        """

        self._value = value

    def __repr__(self):
        return f'Error(value={repr(self._value)})'

    def evaluate(self, variables: Dict[str, Any]) -> Any:
        """Raises an error with a value that was passed during initialisation.

        Raises:
            EvaluationError: Raised on every call. Wraps the error message or
                the exception that was passed during initialisation.
        """

        raise EvaluationError(self._value)
