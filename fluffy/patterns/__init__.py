from fluffy.patterns.case import *
from fluffy.patterns.expressions import *
from fluffy.patterns.match import *
from fluffy.patterns.patterns import *
from fluffy.patterns.variables import *


def demo():
    """A simple demonstration of `match` usage."""

    yield match([1, 2, 3], case | [1, 1, 1] > 1,
                           case | (1, 2, 3) > 2,
                           case | [1, 2, 3] > 3)

    yield match([1, 2, 3], case | [1, 1, 1] > 1,
                           case | otherwise > 2)

    yield match([1, 2, 3], case | [1, 1, 1] > 1,
                           case | [1, x, 1] > +x,
                           case | [1, 1, y] > -y,
                           case | [1, x, y] > (x + y) * 2)

    yield match({'a': 'b'}, case | {'a': 'c'} > 1,
                            case | {'b': 'c'} > 2,
                            case | {'a': 'b'} > 3)

    yield match({'a': 'b', 'c': 'd'}, case | {'a': 'b', 'c': 'd'} > 1)
    yield match({'a': [1, 2, 3]}, case | {'a': [1, x, 3]} > x)
    yield match({'a': 'b'}, case | {x: 'b'} > x)
    yield match({'a': 'b'}, case | {'a': x} > x)
