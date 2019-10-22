# fluffy

A package for functional programming in Python.

## Content

1. [Pattern matching](#pattern-matching)
    1. [Design](#design)
    1. [Matching basic data types](#matching-basic-data-types): `int`, `float`, `complex`, `bool`, `str`
    1. [Matching standard collections](#matching-standard-collections): `list`, `tuple`, `dict`
    1. [Mismatching](#mismatching)
    1. [Variables and expressions](#variables-and-expressions)
1. [Monads](#monads)

## Pattern matching
You can use `fluffy.patterns` for pattern matching.
Here is a simple example:
``` python
from fluffy.patterns import match, case

language = 'german'

greeting = match(language, case | 'english' > 'hello world!',
                           case | 'french'  > 'bonjour monde!',
                           case | 'german'  > 'hallo welt!')

print(greeting)  # Prints 'hallo welt!'.
```

### Design
The main syntax for `match` has the following form:
``` python
match(value, case | pattern[0] > expression[0],
             case | pattern[1] > expression[1],
             case | pattern[2] > expression[2],
             ...)
```

The statement `case | pattern > expression` is evaluated as `((case | pattern) > expression)` due to the priority of operators `|` and `>`.
It returns `Case(pattern, expression)` and is used only for stylistic purposes.

You can also simulate Haskell's syntax for pattern matching like this:
``` python
from fluffy.patterns import match as case, case as of
```

### Matching basic data types
You can match values of built-in types, like `int`, `float`, `complex`, `bool` and `str`, as well as `None`:
``` python
value = ...

match(value, case | 42   > '(natural) answer to the ultimate question',
             case | 42j  > '(complex) answer to the ultimate question',
             case | 42.0 > '(real) answer to the ultimate question',
             ...)
```

### Matching standard collections
You can match lists and tuples:
``` python
from fluffy.patterns import match, case

band = ['Armstrong', 'Dirnt', 'Cool']
name = match(band, case | ['Armstrong', 'Dirnt', 'Cool'] > 'Green Day')

# Or...

band = ('Armstrong', 'Dirnt', 'Cool')
name = match(band, case | ('Armstrong', 'Dirnt', 'Cool') > 'Green Day')
```

### Mismatching
Be careful! You may get an error in a case when there are no matching patterns:
``` python
# Raises a `MismatchError`.
match(0, case | +1 > 'positive',
         case | -1 > 'negative')
```

You can use `_` (or its alias `otherwise`) to handle default cases.
`_` matches any value:
``` python
match(0, case | +1 > 'positive',
         case | -1 > 'negative',
         case |  _ > 'neutral')
```

### Variables and expressions
You can use variables to fetch values and use them later:

``` python
from fluffy.patterns import match, case, x

person = ('Richard', 'Feynman')

surname = match(person, case | ('Albert',  x) > x,
                        case | ('Richard', x) > x)
```

...

## Monads
...
