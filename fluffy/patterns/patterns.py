from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Dict
from dataclasses import is_dataclass

import fluffy.patterns.expressions as expressions


def as_pattern(value: Any) -> 'Pattern':
    """Wraps the `value` into a `Pattern` object."""

    if is_dataclass(value):
        return Dataclass(value)
    elif isinstance(value, list):
        return List(value)
    elif isinstance(value, tuple):
        return Tuple(value)
    elif isinstance(value, dict):
        return Dictionary(value)
    elif isinstance(value, Pattern):
        return value
    elif isinstance(value, expressions.Variable):
        return Variable(value)
    elif any(isinstance(value, cls) for cls in [int, float, bool, str]):
        return Constant(value)

    raise ValueError(f'Value {repr(value)} cannot be converted to a pattern.')


class Pattern(metaclass=ABCMeta):
    """Represents a pattern to match the input value against."""

    @abstractmethod
    def match(self, value: Any) -> Optional[Dict]:
        """Returns either a dictionary of matched variables
        in case of success or none in case of failure."""


class Constant(Pattern):
    """A pattern that matches any constant value."""

    def __init__(self, pattern: Any):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if value == self.pattern:
            return success()
        else:
            return fail()


class Variable(Pattern):
    """A pattern that matches against a variable."""

    def __init__(self, pattern: expressions.Variable):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        return success({self.pattern.name: value})


class List(Pattern):
    """A pattern that matches lists."""

    def __init__(self, pattern: list):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if not isinstance(value, list):
            return fail()

        args = {}
        none = object()

        f = iter(self.pattern)
        g = iter(value)

        while True:
            a = next(f, none)
            b = next(g, none)

            if a is none and b is none:
                return success(args)
            if a is none or b is none:
                return fail()

            if (x := as_pattern(a).match(b)) is not None:
                for name in x:
                    if name not in args:
                        args[name] = x[name]
                    else:
                        raise NameError(f"Variable '{name}' has "
                                        f"already been defined.")
            else:
                return fail()


class Tuple(Pattern):
    """A pattern that matches tuples."""

    def __init__(self, pattern: tuple):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


class Dictionary(Pattern):
    """A pattern that matches dictionaries."""

    def __init__(self, pattern: dict):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


class Dataclass(Pattern):
    """A pattern that matches dataclasses."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


def success(args: Optional[Dict] = None):
    return args or {}


def fail():
    return None
