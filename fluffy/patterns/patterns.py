from abc import ABCMeta, abstractmethod
from typing import Any, Optional, Dict
from dataclasses import is_dataclass


def as_pattern(value):
    """Wraps the `value` into a `Pattern` object."""

    if is_dataclass(value):
        return DataclassPattern(value)
    elif isinstance(value, list):
        return ListPattern(value)
    elif isinstance(value, tuple):
        return TuplePattern(value)
    elif isinstance(value, dict):
        return DictPattern(value)
    else:
        return ConstantPattern(value)


class Pattern(metaclass=ABCMeta):
    """Represents a pattern to match the input value against."""

    @abstractmethod
    def match(self, value: Any) -> Optional[Dict]:
        """Returns either a dictionary of matched variables
        in case of success or none in case of failure."""


class DataclassPattern(Pattern):
    """A pattern that matches dataclasses."""

    def __init__(self, pattern):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


class ListPattern(Pattern):
    """A pattern that matches lists."""

    def __init__(self, pattern: list):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


class TuplePattern(Pattern):
    """A pattern that matches tuples."""

    def __init__(self, pattern: tuple):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


class DictPattern(Pattern):
    """A pattern that matches dictionaries."""

    def __init__(self, pattern: dict):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        pass


class ConstantPattern(Pattern):
    """A pattern that matches any constant value."""

    def __init__(self, pattern: Any):
        self.pattern = pattern

    def match(self, value: Any) -> Optional[Dict]:
        if value == self.pattern:
            return {}
        else:
            return None
