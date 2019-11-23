from math import sqrt

from fluffy.monads import monad, Just, Nothing, Maybe, List


def divide(a, b):
    return Just(a / b) if b != 0 else Nothing()


def root(a):
    return Just(sqrt(a)) if a >= 0 else Nothing()


@monad(Maybe)
def f(x, y):
    """f(x, y) = 2 √(x / y)"""

    a = yield divide(x, y)
    b = yield root(a)
    c = 2 * b

    return c


@monad(List)
def triples(n):
    """Pythagorean triples."""

    x = yield List[1, ..., n]
    y = yield List[x, ..., n]
    z = yield List[y, ..., n]

    yield List[(x, y, z),] if x**2 + y**2 == z**2 else \
          List.empty()


print(triples(15))  # Prints 'List[(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]'.
