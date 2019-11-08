from fluffy.patterns import match, case, x, y


def with_lists():
    """This example demonstrates how lists can be matched."""

    expression = [10, '*', 20]

    result = match(expression, case | [x, '+', y] > x + y,
                               case | [x, '-', y] > x - y,
                               case | [x, '*', y] > x * y,
                               case | [x, '/', y] > x / y)

    assert result == 200
