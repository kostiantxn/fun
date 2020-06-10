from fun.patterns import match, case, x, y


def with_lists():
    """This example demonstrates how lists can be matched."""

    expression = [10, '*', 20]

    result = match(expression, case | [x, '+', y] > x + y,
                               case | [x, '-', y] > x - y,
                               case | [x, '*', y] > x * y,
                               case | [x, '/', y] > x / y)

    print(result)  # Prints '200'.


def with_types():
    """This example demonstrates how types can be matched."""

    value = 'amazing'

    result = match(value, case | x[:int] > x + 451,
                          case | x[:str] > 'wow, ' + x)

    print(result)  # Prints 'wow, amazing'.
