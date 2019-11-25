# fluffy

[![License](https://img.shields.io/github/license/konstantin-ogulchansky/fluffy)](https://github.com/konstantin-ogulchansky/fluffy/blob/master/LICENSE)
[![Workflow](https://github.com/konstantin-ogulchansky/fluffy/workflows/Python%20package/badge.svg)](https://github.com/konstantin-ogulchansky/fluffy/actions?query=workflow%3A%22Python+package%22)

_A package for functional programming in Python._

`fluffy` contains implementations of some features you can find in functional languages such as Haskell.
Those features are not implemented by default in any standard library, and that's why `fluffy` may come in handy.
The `fluffy` package includes:

  * Pattern matching. [[1]](https://github.com/konstantin-ogulchansky/fluffy/tree/master/docs/guide.md#pattern-matching)
  * Monads. [[2]](https://github.com/konstantin-ogulchansky/fluffy/tree/master/docs/guide.md#monads)

## Examples

#### Pattern matching
You can use `fluffy.patterns` for pattern matching.
Here is a simple example:

``` python
from fluffy.patterns import match, case

language = 'French'

greeting = match(language, case | 'English' > 'Hello, world!',
                           case | 'French'  > 'Bonjour le monde!',
                           case | 'German'  > 'Hallo Welt!')

print(greeting)  # Prints 'Bonjour le monde!'.
```

But not only strings can be matched.
You can use the package to match almost anything you could think of: primitive built-in types (`int`, `float`, `complex`, `bool`, `str`), standard collections (`list`, `tuple` and `dict`), data classes.

Sometimes you may need to use variables in pattern matching.
The `fluffy.patterns` package provides an ability to achieve this.
Here is an example:

``` python
from fluffy.patterns import match, case, x, y

expression = [10, '*', 20]

result = match(expression, case | [x, '+', y] > x + y,
                           case | [x, '-', y] > x - y,
                           case | [x, '*', y] > x * y,
                           case | [x, '/', y] > x / y)

print(result)  # Prints '200'.
```

Read the [guide](https://github.com/konstantin-ogulchansky/fluffy/tree/master/docs/guide.md#pattern-matching) or check out the [examples](https://github.com/konstantin-ogulchansky/fluffy/tree/master/examples/patterns.py) to find out more about pattern matching with `fluffy.patterns`.

#### Monads
The `fluffy.monads` package allows you to write monadic functions:

``` python
from math import sqrt
from fluffy.monads import monad, Maybe, Just, Nothing

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

print(f(18, 2))  # Prints 'Just 6.0'.
print(f(18, 0))  # Prints 'Nothing'.
print(f(-8, 2))  # Prints 'Nothing'.
```

You can use `List` as well:
``` python
from fluffy.monads import monad, List

@monad(List)
def triples(n):
    """Pythagorean triples."""

    x = yield List[1, ..., n]
    y = yield List[x, ..., n]
    z = yield List[y, ..., n]

    yield List[(x, y, z),] if x**2 + y**2 == z**2 else \
          List.empty()

print(triples(15))  # Prints 'List[(3, 4, 5), (5, 12, 13), (6, 8, 10), (9, 12, 15)]'.
```

The `monad` decorator allows you to utilise the notation similar to the `do` notation in Haskell.
Thus, a function being wrapped by this decorator must use only a fixed set of statements.
Below you can see the table with allowed statements and their equivalent in Haskell.

| Python        | Haskell       |
| ------------- | ------------- |
| `x = g(y)`    | `let x = g y` |
| `x = yield m` | `x <- m`      |
| `yield m`     | `m`           |
| `return x`    | `return x`    |

You can read more about `fluffy.monads` in the [guide](https://github.com/konstantin-ogulchansky/fluffy/tree/master/docs/guide.md#monads).

## Motivation
...

## Installation
...

## Learn more
Check out the [docs](https://github.com/konstantin-ogulchansky/fluffy/tree/master/docs). <br>
Check out the [examples](https://github.com/konstantin-ogulchansky/fluffy/tree/master/examples).

## Plan
- [x] Pattern matching
- [x] Monads
- [ ] Type classes
- [ ] Immutable data structures

## License
The package is licensed under the [MIT](https://github.com/konstantin-ogulchansky/fluffy/blob/master/LICENSE) License.
