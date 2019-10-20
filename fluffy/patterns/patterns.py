from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Dict, Union
from dataclasses import is_dataclass

import fluffy.patterns.expressions as expressions


def as_pattern(value: Any) -> 'Pattern':
    """Wraps the `value` into a `Pattern` object."""

    if is_dataclass(value):
        return Dataclass(value)
    elif isinstance(value, (int, float, complex, bool, str)):
        return Constant(value)
    elif isinstance(value, (list, tuple, range)):
        return Sequence(value)
    elif isinstance(value, dict):
        return Dictionary(value)
    elif isinstance(value, Pattern):
        return value
    elif isinstance(value, expressions.Variable):
        return Variable(value.name)

    raise ValueError(f'Value {repr(value)} cannot be '
                     f'converted to a pattern.')


class Pattern(metaclass=ABCMeta):
    """Represents a pattern to match the input value against."""

    @abstractmethod
    def match(self, value: Any) -> Optional[Dict]:
        """Returns either a dictionary of matched variables
        in case of success or none in case of failure."""


class Constant(Pattern):
    """A pattern that matches a constant value."""

    def __init__(self, pattern: Any):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if value == self.pattern:
            return success()
        else:
            return fail()


class Variable(Pattern):
    """A pattern that matches against a variable."""

    def __init__(self, name: str):
        self.name = name

    def match(self, value: Any) -> Optional[Dict]:
        return success({self.name: value})


class Sequence(Pattern):
    """A pattern that matches sequences (like lists or tuples)."""

    def __init__(self, pattern: Union[list, tuple]):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if not isinstance(value, type(self.pattern)):
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


class Dictionary(Pattern):
    """A pattern that matches dictionaries."""

    def __init__(self, pattern: dict):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if not isinstance(value, dict):
            return fail()

        args = {}
        value = dict(value)

        for pkey, pvalue in self.pattern.items():
            pkey, pvalue = as_pattern(pkey), as_pattern(pvalue)
            found = None

            for vkey, vvalue in value.items():
                x = pkey.match(vkey)
                y = pvalue.match(vvalue)

                if x is not None and y is not None:
                    # todo: check name collisions
                    args.update(x)
                    args.update(y)
                    found = vkey

                    # todo:
                    #   don't break and try to find any other matches
                    #   raise an error in case of double match
                    break

            if found is None:
                return fail()
            else:
                value.pop(found)

        if len(value) > 0:
            return fail()
        else:
            return success(args)


class Dataclass(Pattern):
    """A pattern that matches dataclasses."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        raise NotImplemented


class Regex(Pattern):
    """A pattern that matches regex groups."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        raise NotImplemented


def success(args: Optional[Dict] = None):
    return args or {}


def fail():
    return None
