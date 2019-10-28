from typing import Dict, Any

import pytest

from fluffy.patterns import match, case, x, Expression, MismatchError


def test_match_return_value():
    """Test that `match` evaluates and returns the first matched expression."""

    result = match(1, case | 1 > 5,
                      case | 1 > 7)

    assert result == 5


def test_match_raising_error():
    """Test that `match` raises `MismatchError` when there are no
    matching cases."""

    with pytest.raises(MismatchError):
        match(1, case | 2 > -2,
                 case | 3 > -3)


def test_match_evaluates_expression():
    """Test that `match` evaluates the expression."""

    class Test(Expression):

        def __init__(self, value):
            self.evaluated = False
            self.variables = None
            self.value = value

        def evaluate(self, variables: Dict[str, Any]) -> Any:
            self.evaluated = True
            self.variables = variables
            return self.value

    expr = Test('value')
    result = match([1, 2], case | [1, x] > expr)

    assert result == 'value'
    assert expr.evaluated
    assert expr.variables == {'x': 2}
