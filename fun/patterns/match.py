from typing import Any

from fun.patterns.case import Case
from fun.patterns.errors import MismatchError


def match(value: Any, *cases: Case):
    """Matches the input value against the specified patterns.

    Checks whether any pattern in the specified list of cases matches the input
    value. In a case when such a pattern was found, the corresponding
    expression is evaluated. The patterns are checked in the same order as they
    were passed to the function. In a case when a matching pattern was not
    found, an error is raised.

    Args:
        value: An input value to match.
        cases: A list of cases to match the input value against.

    Raises:
        MismatchError: Raised when there is no case with a pattern that matches
            the input value.

    Examples:
        >>> from fun.patterns.case import case

        >>> match(2, case | 1 > 'a',
        ...          case | 2 > 'b')
        'b'

        >>> match(1, case | 1 > 'a',
        ...          case | 1 > 'b')
        'a'

        >>> match(3, case | 1 > 'a',
        ...          case | 2 > 'b')
        Traceback (most recent call last):
            ...
        fluffy.patterns.errors.MismatchError: Could not match 3.
    """

    for pattern, expression in cases:
        result = pattern.match(value)
        if result.is_success():
            return expression.evaluate(result.variables)

    raise MismatchError(f"Could not match {repr(value)}.")
