from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Dict, Union, Type
from dataclasses import is_dataclass, fields

from fun.patterns.expressions import Variable


def pattern(value: Any) -> 'Pattern':
    """Creates an instance of `Pattern` from the specified value.

    Args:
        value: A value to create an instance of `Pattern` from.

    Returns:
        An instance of `Pattern` that was constructed depending on
        the specified value.

    Examples:
        >>> pattern(42)
        FixedPattern(value=42)

        >>> pattern([451, 1984])
        SequencePattern(value=[451, 1984])

    Raises:
        TypeError: Raised when the type of the specified value is not
            supported and an instance of `Pattern` cannot be created.
    """

    if isinstance(value, Pattern):
        return value
    elif isinstance(value, (int, float, complex, bool, str)):
        return FixedPattern(value)
    elif isinstance(value, (list, tuple, range)):
        return SequencePattern(value)
    elif isinstance(value, dict):
        return DictionaryPattern(value)
    elif isinstance(value, Variable):
        return VariablePattern(value.name)
    elif isinstance(value, type):
        return TypePattern(value)
    elif is_dataclass(value):
        return DataclassPattern(value)

    raise TypeError(f'{value} cannot be converted to a pattern.')


class Match:
    """Represents the result of a match.

    Represents either a successful or a failed match. Contains a dictionary of
    matched variables in a case of success.

    Attributes:
        variables (dict, optional): A dictionary that maps the names of matched
            variables to the values of those variables. Will be None in a case
            if the match was not successful.
    """

    def __init__(self, variables: Optional[Dict]):
        self.variables = variables

    def is_success(self) -> bool:
        """Returns True if the match is successful and False otherwise."""
        return self.variables is not None

    def is_failure(self) -> bool:
        """Returns True if the match is failed and False otherwise."""
        return self.variables is None

    @classmethod
    def success(cls, variables: Optional[Dict] = None) -> 'Match':
        """Creates an instance of `Match` representing success."""
        return Match(variables or {})

    @classmethod
    def failure(cls) -> 'Match':
        """Creates an instance of `Match` representing failure."""
        return Match(None)

    @classmethod
    def merge(cls, a: 'Match', b: 'Match') -> 'Match':
        """Merges two instances of `Match` together.

        Returns a failure in a case if either of `a` and `b` is a failure.
        Otherwise returns a new successful match with merged matched variables
        of `a` and `b`.

        Args:
            a: An instance of `Match`.
            b: An instance of `Match`.

        Returns:
            A new instance of `Match`.

        Raises:
            NameError: Raised in a case when both `a` and `b` are successful
                matches, and they both have a variable with the same name.
        """

        if a.is_failure() or b.is_failure():
            return Match.failure()
        else:
            variables = dict(a.variables)

            for name in b.variables:
                if name not in variables:
                    variables[name] = b.variables[name]
                else:
                    raise NameError(f"Variable '{name}' has "
                                    f"already been defined.")

            return Match.success(variables)


class Pattern(metaclass=ABCMeta):
    """Represents a pattern that matches specific values."""

    @abstractmethod
    def match(self, value: Any) -> Match:
        """Checks whether the pattern matches the specified value.

        Returns an instance of `Match` that represents either
        a success if the pattern matches the value or a failure otherwise.

        Args:
            value: A value to check.

        Returns:
            Match: A successful `Match` if the pattern matches the specified
                value and a failed `Match` otherwise.
        """


class FixedPattern(Pattern):
    """A pattern that matches a fixed value.

    Matches only values that are equal to the specified fixed value. Does not
    fetch any variables.

    Attributes:
        value: A fixed value to match against.

    Examples:
        >>> p = FixedPattern(1)
        >>> p.match(1).is_success()
        True
        >>> p.match('x').is_success()
        False
    """

    def __init__(self, value: Any):
        self.value = value

    def __repr__(self):
        return f'FixedPattern(value={repr(self.value)})'

    def match(self, value: Any) -> Match:
        """Checks whether the input value is equal to the fixed value."""

        if value == self.value:
            return Match.success()
        else:
            return Match.failure()


class VariablePattern(Pattern):
    """A pattern that matches a variable.

    Matches any value. Fetches that value and associates it with the name of
    the variable.

    Attributes:
        name (str): The name of the variable to associate the value with.

    Examples:
        >>> match = VariablePattern('x').match([1, 2])
        >>> match.is_success()
        True
        >>> match.variables
        {'x': [1, 2]}
    """

    def __init__(self, name: Optional[str]):
        self.name = name

    def __repr__(self):
        return f'VariablePattern(name={repr(self.name)})'

    def match(self, value: Any) -> Match:
        """Matches any value and associates it with the specified name."""

        if self.name is not None:
            return Match.success({self.name: value})
        else:
            return Match.success()


class SequencePattern(Pattern):
    """A pattern that matches a sequence (lists, tuples, ranges).

    Matches input values that have the same type and length as the specified
    sequence, and if every pattern at the i-th position of the specified
    sequence matches the item at the i-th position of the input value. Merges
    the results of those matches.

    Attributes:
        value: A sequence to match against.

    Examples:
        >>> p = SequencePattern([1, 2, 3])
        >>> p.match([1, 2, 3]).is_success()
        True
        >>> p.match([1, 2, 0]).is_success()
        False
    """

    def __init__(self, value: Union[list, tuple, range]):
        self.value = value

    def __repr__(self):
        return f'SequencePattern(value={repr(self.value)})'

    def match(self, value: Any) -> Match:
        """Checks whether the specified sequence matches the input value."""

        if not isinstance(value, type(self.value)):
            return Match.failure()

        success = Match.success()
        nothing = object()

        ps = iter(self.value)
        vs = iter(value)

        while True:
            p = next(ps, nothing)
            v = next(vs, nothing)

            if p is nothing and v is nothing:
                return success
            if p is nothing or v is nothing:
                return Match.failure()

            match = pattern(p).match(v)

            if match.is_success():
                success = Match.merge(success, match)
            else:
                return Match.failure()


class DictionaryPattern(Pattern):
    """A pattern that matches a dictionary.

    For each key-value pair in the input dictionary checks whether there exists
    one and only one key-value pair in the pattern dictionary that matches the
    first pair. Merges the results of those matches.

    Attributes:
        value: A dictionary pattern to match values against.

    Examples:
        >>> p = DictionaryPattern({'a': 'b'})
        >>> p.match({'a': 'b'}).is_success()
        True
        >>> p.match({'a': 'c'}).is_success()
        False
        >>> p.match({'a': 'b', 'c': 'd'}).is_success()
        False
    """

    def __init__(self, value: dict):
        self.value = value

    def __repr__(self):
        return f'DictionaryPattern(value={repr(self.value)})'

    def match(self, value: Any) -> Match:
        """Checks whether the specified dictionary matches the input value.

        Raises:
            ValueError: Raised when a single pattern pair matches more than
                one input pairs.
        """

        if not isinstance(value, dict):
            return Match.failure()

        ps = list(self.value.items())
        vs = list(value.items())

        if len(ps) != len(vs):
            return Match.failure()

        success = Match.success()
        mapping = dict()

        for i, p in enumerate(ps):
            for j, v in enumerate(vs):
                x = pattern(p[0]).match(v[0])  # Match keys.
                y = pattern(p[1]).match(v[1])  # Match values.

                if x.is_failure() or y.is_failure():
                    continue

                if i in mapping.keys():
                    raise ValueError(f'Pattern {p} matches multiple values.')
                if j in mapping.values():
                    raise ValueError(f'Value {v} matches multiple patterns.')

                mapping[i] = j

                success = Match.merge(success, x)
                success = Match.merge(success, y)

            # If the pattern pair does not match any value pair.
            if i not in mapping:
                return Match.failure()

        return success


class DataclassPattern(Pattern):
    """A pattern that matches a dataclass.

    Matches only values that have the same type as the pattern, and every field
    of the pattern matches the same fields of the input value. Merges the
    results of those matches.

    Attributes:
        value: An instance of some dataclass to match values against.

    Examples:
        >>> from dataclasses import dataclass

        >>> @dataclass
        ... class Vector:
        ...     x: int
        ...     y: int

        >>> p = DataclassPattern(Vector(1, 2))
        >>> p.match(Vector(1, 2)).is_success()
        True
        >>> p.match(Vector(2, 3)).is_success()
        False
    """

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'DataclassPattern(value={repr(self.value)})'

    def match(self, value: Any) -> Match:
        """Checks whether the specified pattern matches the input value."""

        if not isinstance(value, type(self.value)):
            return Match.failure()

        success = Match.success()

        for field in fields(value):
            p = getattr(self.value, field.name)
            v = getattr(value, field.name)

            match = pattern(p).match(v)

            if match.is_success():
                success = Match.merge(success, match)
            else:
                return Match.failure()

        return success


class TypePattern(Pattern):
    """A pattern that matches values of the specified type.

    Matches only values that have the same type as the specified one. Fetches
    the matched value in a case if the name of a variable was specified.

    Attributes:
        value (type): A type to match values against.
        variable (str, optional): The name of the variable to associate the
            value with.
    """

    def __init__(self, value: Type, variable: Optional[str] = None):
        self.value = value
        self.variable = variable

    def __repr__(self):
        return f'TypePattern(' \
                   f'value={repr(self.value)}, ' \
                   f'variable={repr(self.variable)}' \
               f')'

    def match(self, value: Any) -> Match:
        """Checks whether the value has the same type as the specified one."""

        if isinstance(value, self.value):
            if self.variable is not None:
                return Match.success({self.variable: value})
            else:
                return Match.success()
        else:
            return Match.failure()
