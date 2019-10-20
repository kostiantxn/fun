from fluffy.patterns.case import *
from fluffy.patterns.expressions import *
from fluffy.patterns.match import *
from fluffy.patterns.patterns import *
from fluffy.patterns.variables import *


def demo():
    """A simple demonstration of `match` usage."""

    yield match([1, 2, 3], case | [1, 1, 1] > 1,
                           case | [1, 2, 3] > 2,
                           case | otherwise > 0)

    yield match([1, 2, 3], case | [1, 1, 1] > 1,
                           case | [1, 2, x] > (x + 10) * 2)

    yield match([1, 2, 3], case | (1, 2, 3) > 1,
                           case | [1, 2, 3] > 2)
