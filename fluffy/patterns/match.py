from typing import Any

from fluffy.patterns.case import Case
from fluffy.patterns.errors import MismatchError


def match(value: Any, *cases: Case):
    """Checks whether any pattern matches the specified value and evaluates
     the corresponding expression in such case. Otherwise raises
     `MismatchError`.

    :param value: input value to match
    :param cases: list of cases to match the input against
    """

    for pattern, expression in cases:
        result = pattern.match(value)
        if result.is_success():
            return expression.evaluate(result.variables)

    raise MismatchError(f"Could not match {repr(value)}.")
