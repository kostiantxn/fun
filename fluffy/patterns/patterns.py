from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Dict, Union
from dataclasses import is_dataclass, fields

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
    elif isinstance(value, type):
        return Type(value)
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
    """A pattern that matches a variable."""

    def __init__(self, name: Optional[str]):
        self.name = name

    def match(self, value: Any) -> Optional[Dict]:
        if self.name is not None:
            return success({self.name: value})
        else:
            return success()


class Sequence(Pattern):
    """A pattern that matches sequences (lists, tuples, ranges)."""

    def __init__(self, pattern: Union[list, tuple, range]):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if not isinstance(value, type(self.pattern)):
            return fail()

        args = {}
        none = object()

        ps = iter(self.pattern)
        vs = iter(value)

        while True:
            p = next(ps, none)
            v = next(vs, none)

            if p is none and v is none:
                return success(args)
            if p is none or v is none:
                return fail()

            if (x := as_pattern(p).match(v)) is not None:
                merge(x, into=args)
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
                    if found is not None:
                        raise ValueError(f'Pattern ({pkey}: {pvalue}) '
                                         f'matches multiple pairs.')

                    merge(x, into=args)
                    merge(y, into=args)

                    found = vkey

            if found is not None:
                value.pop(found)
            else:
                return fail()

        if len(value) > 0:
            return fail()
        else:
            return success(args)


class Dataclass(Pattern):
    """A pattern that matches dataclasses."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if not isinstance(value, type(self.pattern)):
            return fail()

        args = {}

        for field in fields(value):
            p = getattr(self.pattern, field.name)
            v = getattr(value, field.name)

            if (x := as_pattern(p).match(v)) is not None:
                merge(x, into=args)
            else:
                return fail()

        return success(args)


class Type(Pattern):
    """A pattern that matches types of input values."""

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


def merge(args: Dict, into: Dict):
    """Merges one dictionary into another one."""

    for name in args:
        if name not in into:
            into[name] = args[name]
        else:
            raise NameError(f"Variable '{name}' has "
                            f"already been defined.")
