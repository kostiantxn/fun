# fluffy

A package for functional programming in Python.

### Contents

1. [Pattern matching](#pattern-matching)
1. [Monads](#monads)

## Pattern matching
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

The main syntax for `match` has the following form:
``` python
match(value, case | pattern[0] > expression[0],
             case | pattern[1] > expression[1],
             case | pattern[2] > expression[2],
             ...)
```

The `match` function goes through the list of cases in the same order as they are passed and tries to find the first pattern that matches the input value.
In a case if a pattern that matches the input value exists, an expression corresponding to that pattern is evaluated:
``` python
result = match(42, case | 42 > 'a',
                   case | 42 > 'b')
                   
print(result)  # Prints 'a'.
```
Otherwise, a `MismatchError` is raised:
``` python
# Raises a `MismatchError`.
match(0, case | +1 > 'positive',
         case | -1 > 'negative')
```

### Match `int`, `float`, `complex`, `bool`, `str` and `None`
You can match simple built-in types:
``` python
match(value, case | 42    > "Matches 42    of `int`.",
             case | 42.0  > "Matches 42.0  of `float`.",
             case | 42j   > "Matches 42j   of `complex`.",
             case | True  > "Matches True  of `bool`.",
             case | '451' > "Matches '451' of `str`.",
             case | None  > "Matches None.")
```


### Match variables
You can match variables to fetch values and use them later:

``` python
from fluffy.patterns import match, case, x

direction = 'Q'

result = match(direction, case | 'W' > "Moving up.",
                          case | 'S' > "Moving down.",
                          case | 'A' > "Moving left.",
                          case | 'D' > "Moving right."
                          case |  x  > "Unknown direction: " + x)

print(result)  # Prints 'Unknown direction: Q'.
```

You can use operators on expressions:
``` python
# Unary operators.
match(value, case | x > +x)
match(value, case | x > -x)
match(value, case | x > abs(x))

# Binary operators.
match(value, case | x > x + 1)
match(value, case | x > x - 2)
match(value, case | x > x * 3)
match(value, case | x > x / 4)

# And others...
```

You can also apply functions to expressions:
``` python
from math import sqrt
from fluffy.pattern import match, case, x, apply

match(42, case | x > apply(sqrt, x))
```

_Note:_ you cannot simply write `case | x > sqrt(x)` since `sqrt(x)` will be evaluated _before_ the value for `x` is matched.

There are plenty of predefined variables: `a`, `b`, `c`, ..., `x`, `y`, `z`.
You can also define your own variables if you need to:
``` python
from fluffy.patterns import Variable, variables

a = Variable('a')        # Defines a single variable.
b, c = variables('b c')  # Defines multiple variables.
```

You can discard unneeded values with the special variable `_` (or its alias `otherwise`).
This allows you to handle default cases:
``` python
match(0, case | +1 > 'positive',
         case | -1 > 'negative',
         case |  _ > 'neutral')
```

_Note:_ the `_` variable (as well as `otherwise`) cannot be used as an expression. The following code will not work:
``` python
match(value, case | _ > 'This will not work: ' + _)
```

### Match `list`, `tuple` and `dict`
You can match lists and tuples:
``` python
match(value, case | [1, 2, 3] > "Matches a list  [1, 2, 3].",
             case | (1, 2, 3) > "Matches a tuple (1, 2, 3).")
```

As you would expect, `fluffy.patterns` allows to match variables inside lists and tuples:
``` python
result = match([1, 2, 3], case | [1, 2, x] > x)

print(result)  # Prints '3'.
```

But be careful: you cannot use the same variable twice within a single pattern. For example, the following code will cause an error:
``` python
match([1, 2, 3], case | [1, x, x] > x)  # Raises `NameError`.
```

To achive the result, you should use different variables:
``` python
from fluffy.pattern import match, case, x, y

result = match([1, 2, 3], case | [1, x, y] > x + y)

print(result)  # Prints '5'.
```

You can also match dictionaries:
``` python
match(value, case | {1: 2, 'a': 'b'} > "Matches dictionaries that have exactly "
                                       "two key-value pairs: (1, 2) and ('a', 'b').")
```

### Match data classes
...

### Raise errors
You can raise an error of any type:
``` python
from fluffy.patterns import match, case, error

match('x', case | 'x' > error('message'))  # Raises `EvaluationError('message')`.
```

## Monads
You can use `fluffy.monads` to write monadic functions.
Here is an example:
``` python
from fluffy.monads import monad, List

@monad(List)
def pairs(n):
    x = yield List[1, ..., n]
    y = yield List[x, ..., n]

    return (x, y)

print(pairs(3))  # Prints 'List[(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]'.
```
