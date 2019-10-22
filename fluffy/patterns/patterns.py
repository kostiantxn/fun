from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Dict, Union
from dataclasses import is_dataclass, fields

from fluffy.patterns.expressions import Variable


def as_pattern(value: Any) -> 'Pattern':
    """Converts `value` into a `Pattern` object."""

    if isinstance(value, Pattern):
        return value
    elif isinstance(value, (int, float, complex, bool, str)):
        return ConstantPattern(value)
    elif isinstance(value, (list, tuple, range)):
        return SequencePattern(value)
    elif isinstance(value, dict):
        return DictionaryPattern(value)
    elif isinstance(value, Variable):
        return VariablePattern(value.name)
    elif is_dataclass(value):
        return DataclassPattern(value)

    raise ValueError(f'{repr(value)} cannot be converted to a pattern.')


class Match:
    """Represents the result of a match.
    Contains a dictionary of matched variables in the case of success."""

    def __init__(self, variables: Optional[Dict] = None):
        self.variables = variables

    def is_success(self) -> bool:
        return self.variables is not None

    def is_failure(self) -> bool:
        return self.variables is None

    @classmethod
    def success(cls, variables: Optional[Dict] = None) -> 'Match':
        return Match(variables or {})

    @classmethod
    def failure(cls) -> 'Match':
        return Match()

    @classmethod
    def merge(cls, a: 'Match', b: 'Match') -> 'Match':
        """Merges two matching results together."""

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
    """Represents a pattern to match the input value against."""

    @abstractmethod
    def match(self, value: Any) -> Match:
        """Checks whether the specified value matches the pattern
        and returns an instance of `Match` that represents either
        a success with matched variables or a failure."""


class ConstantPattern(Pattern):
    """A pattern that matches constant values."""

    def __init__(self, pattern: Any):
        self.pattern = pattern

    def match(self, value: Any) -> Match:
        if value == self.pattern:
            return Match.success()
        else:
            return Match.failure()


class VariablePattern(Pattern):
    """A pattern that matches variables."""

    def __init__(self, name: Optional[str]):
        self.name = name

    def match(self, value: Any) -> Match:
        if self.name is not None:
            return Match.success({self.name: value})
        else:
            return Match.success()


class SequencePattern(Pattern):
    """A pattern that matches sequences (lists, tuples, ranges)."""

    def __init__(self, pattern: Union[list, tuple, range]):
        self.pattern = pattern

    def match(self, value: Any) -> Match:
        if not isinstance(value, type(self.pattern)):
            return Match.failure()

        success = Match.success()
        nothing = object()

        ps = iter(self.pattern)
        vs = iter(value)

        while True:
            p = next(ps, nothing)
            v = next(vs, nothing)

            if p is nothing and v is nothing:
                return success
            if p is nothing or v is nothing:
                return Match.failure()

            if (match := as_pattern(p).match(v)).is_success():
                success = Match.merge(success, match)
            else:
                return Match.failure()


class DictionaryPattern(Pattern):
    """A pattern that matches dictionaries."""

    def __init__(self, pattern: dict):
        self.pattern = pattern

    def match(self, value: Any) -> Match:
        if not isinstance(value, dict):
            return Match.failure()

        success = Match.success()
        value = dict(value)

        for pkey, pvalue in self.pattern.items():
            pkey, pvalue = as_pattern(pkey), as_pattern(pvalue)
            found = None

            for vkey, vvalue in value.items():
                x = pkey.match(vkey)
                y = pvalue.match(vvalue)

                if x.is_success() and y.is_success():
                    if found is not None:
                        raise ValueError(f'Pattern ({pkey}: {pvalue}) '
                                         f'matches multiple pairs.')

                    success = Match.merge(success, x)
                    success = Match.merge(success, y)

                    found = vkey

            if found is not None:
                value.pop(found)
            else:
                return Match.failure()

        if len(value) > 0:
            return Match.failure()
        else:
            return success


class DataclassPattern(Pattern):
    """A pattern that matches dataclasses."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Match:
        if not isinstance(value, type(self.pattern)):
            return Match.failure()

        success = Match.success()

        for field in fields(value):
            p = getattr(self.pattern, field.name)
            v = getattr(value, field.name)

            if (match := as_pattern(p).match(v)).is_success():
                success = Match.merge(success, match)
            else:
                return Match.failure()

        return success


class TypePattern(Pattern):
    """A pattern that matches types."""

    def __init__(self, pattern, variable):
        self.pattern = pattern
        self.variable = variable

    def match(self, value: Any) -> Match:
        if isinstance(value, self.pattern):
            if self.variable is not None:
                return Match.success({self.variable: value})
            else:
                return Match.success()
        else:
            return Match.failure()


class RegexPattern(Pattern):
    """A pattern that matches regular expressions."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Match:
        raise NotImplemented
